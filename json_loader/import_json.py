import psycopg2
import requests

import create_tables as c
import insert_tables as i
import create_event_types as create
import populate_event_types as populate

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
        if json_data:
            if add_match_id:
                match_id = int(path.split('/')[1].replace('.json', ''))
                for i in range(0, len(json_data)):
                    json_data[i]['match_id'] = match_id
            data.extend(json_data)
    return data

print('Fetching data from GitHub...')

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

# get the events data
events_data = get_json_data_from_paths(events_paths, True)
print(f'Fetched events data from GitHub (length: {len(events_data)}).')
print()

# ADDING AND CONNECTING TO THE POSTGRESQL DB =================================
print('Starting to populate tables in PostgreSQL...')
print()

def insert_managers(match : dict, team : str):
    if 'managers' in match[team]:
        manager = match[team]['managers'][0]
        manager_id = manager['id']
        manager_values = (manager_id, manager['name'], manager['nickname'],
                        manager['dob'], manager['country']['name'],
                        manager_id)
        cur.execute(i.managers_query, manager_values)

def insert_teams(match : dict, team : str):
    team_dict = match[team]
    team_id = team_dict[team + '_id']
    manager_id = None
    if 'managers' in team_dict:
        manager_id = team_dict['managers'][0]['id']
    team_values = (team_id, team_dict[team + '_name'],
                   team_dict[team + '_gender'], team_dict[team + '_group'],
                   team_dict['country']['name'], manager_id, team_id)
    cur.execute(i.teams_query, team_values)

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

# FIXME: i can't add this as a FK because competition_id is not unique in the competitions table
# FOREIGN KEY (competition_id) REFERENCES competitions (competition_id),

cur = conn.cursor() # a cursor object to execute SQL commands

cur.execute(c.create_tables_query) # execute the CREATE TABLE statement
conn.commit() # commit the transaction

# prepare and execute the INSERT statement for each item in valid_comp_data
print('Populating PostgreSQL from competitions.json...')
for comp in valid_comp_data:
    # populate the seasons table
    season_id = comp['season_id']
    seasons_values = (season_id, comp['season_name'], season_id)
    cur.execute(i.seasons_query, seasons_values)

    # populate the competitions table
    season_name = comp['season_name']
    comp_values = (comp['competition_id'], comp['season_id'],
                   comp['country_name'], comp['competition_name'],
                   comp['competition_gender'], comp['competition_youth'],
                   comp['competition_international'], season_name,
                   season_name)
    cur.execute(i.competitions_query, comp_values)

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
        cur.execute(i.stadiums_query, stadium_values)

    # populate the referees table
    if 'referee' in match:
        referee = match['referee']
        referee_id = referee['id']
        referee_values = (referee_id, referee['name'],
                          referee['country']['name'], referee_id)
        cur.execute(i.referees_query, referee_values)

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
    cur.execute(i.matches_query, match_values)

conn.commit() # commit the transaction
print('Populated the managers table.')
print('Populated the teams table.')
print('Populated the stadiums table.')
print('Populated the referees table.')
print('Populated the matches table.')
print()

print('Populating PostreSQL from lineups.json...')
card_id = 1     # create id numbers to add to the cards table
for lineup in lineups_data:
    match_id = lineup['match_id']
    players = lineup['lineup']

    # populate lineups table
    team_id = lineup['team_id']
    player_ids = [ p['player_id'] for p in players ]
    lineups_values = (match_id, team_id, lineup['team_name'], player_ids,
                      match_id, team_id)
    cur.execute(i.lineups_query, lineups_values)

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
        cur.execute(i.players_query, player_values)

        # populate the cards table
        for values in card_values:
            cur.execute(i.cards_query, values)

        # populate the positions table
        for values in position_values:
            cur.execute(i.positions_query, values)

conn.commit() # commit the transaction
print('Populated the lineups table.')
print('Populated the cards table.')
print('Populated the players table.')
print()

# create the event types tables
cur.execute(create.event_type_tables_query)
conn.commit() # commit the transaction

print('Populating PostreSQL from events.json...')
num_events = 1
for event in events_data:
    print(f'{num_events}/{len(events_data)}')
    num_events += 1
    id = event['id']

    # populate the events table
    player_id, position_id, location, duration, under_pressure, off_camera, \
        out, related_events = None, None, None, None, None, None, None, None
    if 'player' in event:
        player_id = event['player']['id']
    if 'position' in event:
        position_id = event['position']['id']
    if 'location' in event:
        location = event['location']
    if 'duration' in event:
        duration = event['duration']
    if 'under_pressure' in event:
        under_pressure = event['under_pressure']
    if 'off_camera' in event:
        off_camera = event['off_camera']
    if 'out' in event:
        out = event['out']
    if 'related_events' in event:
        related_events = event['related_events']
    event_values = (id, event['match_id'], event['index'],
                    event['period'], event['timestamp'], event['minute'],
                    event['type']['name'], event['possession'],
                    event['possession_team']['id'],
                    event['play_pattern']['name'], event['team']['id'],
                    player_id, position_id, location, duration,
                    under_pressure, off_camera, out, related_events, id)
    cur.execute(i.events_query, event_values)

    # populate the event types table
    type_name = event['type']['name']
    if type_name == '50/50' or type_name == 'Bad Behaviour' \
        or type_name == 'Ball Receipt' or type_name == 'Ball Recovery' \
        or type_name == 'Block' or type_name == 'Carry' \
        or type_name == 'Clearance' or type_name == 'Dribble' \
        or type_name == 'Dribbled Past' or type_name == 'Duel' \
        or type_name == 'Foul Committed' or type_name == 'Foul Won' \
        or type_name == 'Goal Keeper' or type_name == 'Half End*' \
        or type_name == 'Half Start*' or type_name == 'Injury Stoppage' \
        or type_name == 'Interception' or type_name == 'Miscontrol' \
        or type_name == 'Pass' or type_name == 'Player Off' \
        or type_name == 'Pressure' or type_name == 'Shot' \
        or type_name == 'Substitution':
        populate.event_type_tables(event)

    # populate the tactics table
    if 'tactics' in event:
        tactics = event['tactics']
        player_ids = [ p['player']['id'] for p in tactics['lineup'] ]
        tactics_values = (id, event['tactics']['formation'], player_ids, id)

conn.commit() # commit the transaction
print('Populated the events table.')
print('Populated the event types tables.')
print('Populated the tactics table.')
print()

# close the cursor and connection
cur.close()
conn.close()