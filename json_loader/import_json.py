import psycopg2
import requests

# import github data only from these seasons
VALID_SEASONS = {
    'La Liga': ['2018/2019', '2019/2020', '2020/2021'],
    'Premier League': ['2003/2004']
}

def import_json_from_github(path : str) -> list:
    '''
    Imports a JSON file from statsbomb's open-data repository on GitHub with
    the specified path.

    Args:
        path (str): A string representing the path of the JSON file.

    Returns:
        A list representing the JSON file.
    '''
    url = f'https://raw.githubusercontent.com/statsbomb/open-data/0067cae/data/{path}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Failed to fetch {path} from GitHub with status code {response.status_code}.')
        return

def get_json_data_from_paths(paths : list[str], add_match_id=False) -> list:
    '''
    Returns a list of data fetched from JSON files at the specified paths.

    Args:
        paths (list[str]): A list of strings representing the paths of the
            JSON files to fetch data from.
    
    Returns:
        A list representing the data fetched from JSON files.
    '''
    data = []
    for path in paths:
        json_data = import_json_from_github(path)
        if add_match_id:
            match_id = int(path.split('/')[1].replace('.json', ''))
            for i in range(0, len(json_data)):
                json_data[i]['match_id'] = match_id
        if json_data:
            data.extend(json_data)
    return data

print('Fetching data from GitHub...')
print()

# get the competitions data
comp_data = get_json_data_from_paths(['competitions.json'])
print(f'Fetched competitions data from GitHub (length: {len(comp_data)}).')

# get the necessary data from comp_data and store it in valid_comp_data
valid_comp_data = []
for comp in comp_data:
    comp_name = comp['competition_name']
    if comp_name in VALID_SEASONS.keys() and comp['season_name'] in VALID_SEASONS[comp_name]:
        valid_comp_data.append(comp)
print(f'Filtered valid competitions data (length: {len(valid_comp_data)}).')

# determine the paths to get the necessary data from matches
matches_paths = []
for comp in valid_comp_data:
    comp_id = comp['competition_id']
    season_id = comp['season_id']
    matches_paths.append(f'matches/{comp_id}/{season_id}.json')

# get the matches data
matches_data = get_json_data_from_paths(matches_paths)
print(f'Fetched matches data from GitHub (length: {len(matches_data)}).')

# determine the paths to get the necessary data from lineups and events
lineups_paths = []
events_paths = []
for match in matches_data:
    match_id = match['match_id']
    lineups_paths.append(f'lineups/{match_id}.json')
    events_paths.append(f'events/{match_id}.json')

# get the lineups data
lineups_data = get_json_data_from_paths(lineups_paths, True)
print(f'Fetched lineups data from GitHub (length: {len(lineups_data)}).')

# # get the events data
# events_data = get_json_data_from_paths(events_paths)
# print(f'Fetched events data from GitHub (length: {len(events_data)}).')
print()

# TESTING ADDING AND CONNECTING TO THE POSTGRESQL DB -------------------------
print('Starting to populate tables in PostgreSQL...')
print()

def insert_managers(match : dict, team : str):
    if 'managers' in match[team]:
        manager = match[team]['managers'][0]
        manager_id = manager['id']
        manager_values = (manager_id, manager['name'], manager['nickname'],
                        manager['dob'], manager['country']['name'],
                        manager_id)
        cur.execute(INSERT_MANAGERS_QUERY, manager_values)

def insert_teams(match : dict, team : str):
    team_dict = match[team]
    team_id = team_dict[team + '_id']
    manager_id = None
    if 'managers' in team_dict:
        manager_id = team_dict['managers'][0]['id']
    team_values = (team_id, team_dict[team + '_name'],
                   team_dict[team + '_gender'], team_dict[team + '_group'],
                   team_dict['country']['name'], manager_id, team_id)
    cur.execute(INSERT_TEAMS_QUERY, team_values)

def get_interval(timestamp : str) -> str:
    if timestamp:
        minutes, seconds = timestamp.split(':')
        return f'{minutes} minutes {seconds} seconds'
    return None

# connect to PostgreSQL database
conn = psycopg2.connect(
    dbname='project_database',
    user='postgres',
    password='postgres',
    host='localhost',
    port='5432'
)

# define the CREATE TABLE statement
CREATE_TABLES_QUERY = '''
    CREATE TABLE IF NOT EXISTS seasons (
        season_id INT PRIMARY KEY,
        season_name VARCHAR(9)
    );
    CREATE TABLE IF NOT EXISTS competitions (
        id SERIAL PRIMARY KEY,
        competition_id INT,
        season_id INT,
        country_name VARCHAR(255),
        competition_name VARCHAR(255),
        competition_gender VARCHAR(255),
        competition_youth BOOLEAN,
        competition_international BOOLEAN,
        season_name VARCHAR(9),
        FOREIGN KEY (season_id) REFERENCES seasons (season_id)
    );
    CREATE TABLE IF NOT EXISTS managers (
        id INT PRIMARY KEY,
        name VARCHAR(255),
        nickname VARCHAR(255),
        dob DATE,
        country_name VARCHAR(255)     
    );
    CREATE TABLE IF NOT EXISTS teams (
        team_id INT PRIMARY KEY,
        team_name VARCHAR(255),
        team_gender VARCHAR(255),
        team_group VARCHAR(255),
        country_name VARCHAR(255),
        manager_id INT,
        FOREIGN KEY (manager_id) REFERENCES managers (id)
    );
    CREATE TABLE IF NOT EXISTS stadiums (
        id INT PRIMARY KEY,
        name VARCHAR(255),
        country_name VARCHAR(255)
    );
    CREATE TABLE IF NOT EXISTS referees (
        id INT PRIMARY KEY,
        name VARCHAR(255),
        country_name VARCHAR(255)
    );
    CREATE TABLE IF NOT EXISTS matches (
        match_id INT PRIMARY KEY,
        match_date DATE,
        kick_off TIME,
        competition_id INT,
        season_id INT,
        home_team_id INT,
        away_team_id INT,
        home_score INT,
        away_score INT,
        match_week INT,
        competition_stage_name VARCHAR(255),
        stadium_id INT,
        referee_id INT,
        FOREIGN KEY (season_id) REFERENCES seasons (season_id),
        FOREIGN KEY (home_team_id) REFERENCES teams (team_id),
        FOREIGN KEY (away_team_id) REFERENCES teams (team_id),
        FOREIGN KEY (stadium_id) REFERENCES stadiums (id),
        FOREIGN KEY (referee_id) REFERENCES referees (id)
    );
    CREATE TABLE IF NOT EXISTS lineups (
        match_id INT,
        team_id INT,
        team_name VARCHAR(255),
        lineup INT[],
        FOREIGN KEY (match_id) REFERENCES matches (match_id)
    );
    CREATE TABLE IF NOT EXISTS players (
        match_id INT,
        player_id INT,
        player_name VARCHAR(255),
        player_nickname VARCHAR(255),
        jersey_number INT,
        country_name VARCHAR(255),
        cards INT[],
        positions INT[],
        PRIMARY KEY (match_id, player_id)
    );
    CREATE TABLE IF NOT EXISTS cards (
        match_id INT,
        player_id INT,
        card_id INT,
        time INTERVAL,
        card_type VARCHAR(255),
        reason VARCHAR(255),
        period INT,
        PRIMARY KEY (card_id),
        FOREIGN KEY (match_id) REFERENCES matches (match_id),
        FOREIGN KEY (match_id, player_id) REFERENCES players (match_id, player_id)
    );
    CREATE TABLE IF NOT EXISTS positions (
        match_id INT,
        player_id INT,
        position_id INT,
        position VARCHAR(255),
        from_time INTERVAL,
        to_time INTERVAL,
        from_period INT,
        to_period INT,
        start_reason VARCHAR(255),
        end_reason VARCHAR(255),
        FOREIGN KEY (match_id) REFERENCES matches (match_id),
        FOREIGN KEY (match_id, player_id) REFERENCES players (match_id, player_id)
    );
'''

# FIXME: i can't add this as a FK because competition_id is not unique in the competitions table
# FOREIGN KEY (competition_id) REFERENCES competitions (competition_id),

INSERT_SEASONS_QUERY = '''
    INSERT INTO seasons (season_id, season_name)
    SELECT
        %s AS season_id,
        %s AS season_name
    WHERE NOT EXISTS (
        SELECT 1
        FROM seasons
        WHERE season_id = %s
    );
'''

INSERT_COMPS_QUERY = '''
    INSERT INTO competitions (competition_id, season_id, country_name,
    competition_name, competition_gender, competition_youth,
    competition_international, season_name)
    SELECT
        %s AS competition_id,
        %s AS season_id,
        %s AS country_name,
        %s AS competition_name,
        %s AS competition_gender,
        %s AS competition_youth,
        %s AS competition_international,
        %s AS season_name
    WHERE NOT EXISTS (
        SELECT 1
        FROM competitions
        WHERE season_name = %s
    );
'''

INSERT_MANAGERS_QUERY = '''
    INSERT INTO managers (id, name, nickname, dob, country_name)
    SELECT
        %s AS id,
        %s AS name,
        %s AS nickname,
        %s AS dob,
        %s AS country_name
    WHERE NOT EXISTS (
        SELECT 1
        FROM managers
        WHERE id = %s
    )
'''

INSERT_TEAMS_QUERY = '''
    INSERT INTO teams (team_id, team_name, team_gender, team_group,
    country_name, manager_id)
    SELECT
        %s AS team_id,
        %s AS team_name,
        %s AS team_gender,
        %s AS team_group,
        %s AS country_name,
        %s AS manager_id
    WHERE NOT EXISTS (
        SELECT 1
        FROM teams
        WHERE team_id = %s
    )
'''

INSERT_STADIUMS_QUERY = '''
    INSERT INTO stadiums (id, name, country_name)
    SELECT
        %s AS id,
        %s AS name,
        %s AS country_name
    WHERE NOT EXISTS (
        SELECT 1
        FROM stadiums
        WHERE id = %s
    )
'''

INSERT_REFEREES_QUERY = '''
    INSERT INTO referees (id, name, country_name)
    SELECT
        %s AS id,
        %s AS name,
        %s AS country_name
    WHERE NOT EXISTS (
        SELECT 1
        FROM referees
        WHERE id = %s
    )
'''

INSERT_MATCHES_QUERY = '''
    INSERT INTO matches (match_id, match_date, kick_off, competition_id,
    season_id, home_team_id, away_team_id, home_score, away_score, match_week,
    competition_stage_name, stadium_id, referee_id)
    SELECT
        %s AS match_id,
        %s AS match_date,
        %s AS kick_off,
        %s AS competition_id,
        %s AS season_id,
        %s AS home_team_id,
        %s AS away_team_id,
        %s AS home_score,
        %s AS away_score,
        %s AS match_week,
        %s AS competition_stage_name,
        %s AS stadium_id,
        %s AS referee_id
    WHERE NOT EXISTS (
        SELECT 1
        FROM matches
        WHERE match_id = %s
    );
'''

INSERT_LINEUPS_QUERY = '''
    INSERT INTO lineups (match_id, team_id, team_name, lineup)
    SELECT
        %s AS match_id,
        %s AS team_id,
        %s AS team_name,
        %s AS lineup
    WHERE NOT EXISTS (
        SELECT 1
        FROM lineups
        WHERE match_id = %s AND team_id = %s
    );
'''

INSERT_PLAYERS_QUERY = '''
    INSERT INTO players (match_id, player_id, player_name, player_nickname,
    jersey_number, country_name, cards, positions)
    SELECT
        %s AS match_id,
        %s AS player_id,
        %s AS player_name,
        %s AS player_nickname,
        %s AS jersey_number,
        %s AS country_name,
        %s AS cards,
        %s AS positions
    WHERE NOT EXISTS (
        SELECT 1
        FROM players
        WHERE match_id = %s AND player_id = %s
    );
'''

INSERT_CARDS_QUERY = '''
    INSERT INTO cards (match_id, player_id, card_id, time, card_type, reason,
    period)
    SELECT
        %s AS match_id,
        %s AS player_id,
        %s AS card_id,
        %s AS time,
        %s AS card_type,
        %s AS reason,
        %s AS period
    WHERE NOT EXISTS (
        SELECT 1
        FROM cards
        WHERE match_id = %s AND player_id = %s AND card_id = %s
    )
'''

INSERT_POSITIONS_QUERY = '''
    INSERT INTO positions (match_id, player_id, position_id, position,
    from_time, to_time, from_period, to_period, start_reason, end_reason)
    SELECT
        %s AS match_id,
        %s AS player_id,
        %s AS position_id,
        %s AS position,
        %s AS from_time,
        %s AS to_time,
        %s AS from_period,
        %s AS to_period,
        %s AS start_reason,
        %s AS end_reason
    WHERE NOT EXISTS (
        SELECT 1
        FROM positions
        WHERE match_id = %s AND player_id = %s AND position_id = %s
    )
'''

cur = conn.cursor() # a cursor object to execute SQL commands

cur.execute(CREATE_TABLES_QUERY) # execute the CREATE TABLE statement
conn.commit() # commit the transaction

# prepare and execute the INSERT statement for each item in valid_comp_data
print('Populating PostgreSQL from competitions.json...')
for comp in valid_comp_data:
    # populate the seasons table
    season_id = comp['season_id']
    seasons_values = (season_id, comp['season_name'], season_id)
    cur.execute(INSERT_SEASONS_QUERY, seasons_values)

    # populate the competitions table
    season_name = comp['season_name']
    comp_values = (comp['competition_id'], comp['season_id'],
                   comp['country_name'], comp['competition_name'],
                   comp['competition_gender'], comp['competition_youth'],
                   comp['competition_international'], season_name,
                   season_name)
    cur.execute(INSERT_COMPS_QUERY, comp_values)

conn.commit() # commit the transaction
print('Populated the seasons table.')
print('Populated the competitions table.')
print()

# NOTE: managers in teams are optional
# NOTE: stadium in matches are optional
# NOTE: referees are optional
print('Populating PostgreSQL from matches.json...')
for match in matches_data:
    # populate the managers table
    insert_managers(match, 'home_team')
    insert_managers(match, 'away_team')

    # populate the teams table
    insert_teams(match, 'home_team')
    insert_teams(match, 'away_team')

    # populate the stadiums table
    if 'stadium' in match:
        stadium = match['stadium']
        stadium_id = stadium['id']
        stadium_values = (stadium_id, stadium['name'], stadium['country']['name'],
                        stadium_id)
        cur.execute(INSERT_STADIUMS_QUERY, stadium_values)

    # populate the referees table
    if 'referee' in match:
        referee = match['referee']
        referee_id = referee['id']
        referee_values = (referee_id, referee['name'],
                          referee['country']['name'], referee_id)
        cur.execute(INSERT_REFEREES_QUERY, referee_values)

    # populate the matches table
    match_id = match['match_id']
    stadium_id, referee_id = None, None
    if 'stadium' in match:
        stadium_id = match['stadium']['id']
    if 'referee' in match:
        referee_id = match['referee']['id']
    match_values = (match_id, match['match_date'], match['kick_off'],
                    match['competition']['competition_id'],
                    match['season']['season_id'],
                    match['home_team']['home_team_id'],
                    match['away_team']['away_team_id'],
                    match['home_score'], match['away_score'],
                    match['match_week'],
                    match['competition_stage']['name'], stadium_id,
                    referee_id, match_id)
    cur.execute(INSERT_MATCHES_QUERY, match_values)

conn.commit() # commit the transaction
print('Populated the managers table.')
print('Populated the teams table.')
print('Populated the stadiums table.')
print('Populated the referees table.')
print('Populated the matches table.')
print()

print('Populating PostreSQL from lineups.json...')
print()
card_id = 1     # create id numbers to add to the cards table
for lineup in lineups_data:
    match_id = lineup['match_id']
    players = lineup['lineup']

    # populate lineups table
    team_id = lineup['team_id']
    player_ids = [ p['player_id'] for p in players ]
    lineups_values = (match_id, team_id, lineup['team_name'], player_ids,
                      match_id, team_id)
    cur.execute(INSERT_LINEUPS_QUERY, lineups_values)

    for player in players:
        player_id = player['player_id']

        # process info regarding the player's cards
        cards = player['cards']
        card_ids = [] # card ids associated with the player
        card_values = [] # values associated with each card
        for card in cards:
            card_values.append((match_id, player_id, card_id,
                                get_interval(card['time']), card['card_type'],
                                card['reason'], card['period'], match_id,
                                player_id, card_id))
            card_ids.append(card_id)
            card_id += 1

        # process info regarding the player's positions
        positions = player['positions']
        position_ids = [] # position ids associated with the player
        position_values = [] # values associated with each position
        for position in positions:
            position_id = position['position_id']
            position_values.append((match_id, player_id, position_id,
                                   position['position'],
                                   get_interval(position['from']),
                                   get_interval(position['to']),
                                   position['from_period'],
                                   position['to_period'],
                                   position['start_reason'],
                                   position['end_reason'], match_id,
                                   player_id, position_id))

        # populate the players table
        player_values = (match_id, player_id, player['player_name'],
                         player['player_nickname'], player['jersey_number'],
                         player['country']['name'], card_ids, position_ids,
                         match_id, player_id)
        cur.execute(INSERT_PLAYERS_QUERY, player_values)

        # populate the cards table
        for values in card_values:
            cur.execute(INSERT_CARDS_QUERY, values)

        # populate the positions table
        for values in position_values:
            cur.execute(INSERT_POSITIONS_QUERY, values)

conn.commit() # commit the transaction
print('Populated the lineups table.')
print('Populated the cards table.')
print('Populated the players table.')
print()

# close the cursor and connection
cur.close()
conn.close()