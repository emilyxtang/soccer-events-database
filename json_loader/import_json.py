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

def get_json_data_from_paths(paths : list[str]) -> list:
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
            data.extend(json_data)
    return data

# get the competitions data
comp_data = get_json_data_from_paths(['competitions.json'])
print(f'Fetched competitions data from GitHub (length: {len(comp_data)})')

# get the necessary data from comp_data and store it in valid_comp_data
valid_comp_data = []
for comp in comp_data:
    comp_name = comp['competition_name']
    if comp_name in VALID_SEASONS.keys() and comp['season_name'] in VALID_SEASONS[comp_name]:
        valid_comp_data.append(comp)
print(f'Filtered valid competitions data (length: {len(valid_comp_data)})')

# determine the paths to get the necessary data from matches
matches_paths = []
for comp in valid_comp_data:
    comp_id = comp['competition_id']
    season_id = comp['season_id']
    matches_paths.append(f'matches/{comp_id}/{season_id}.json')

# get the matches data
matches_data = get_json_data_from_paths(matches_paths)
print(f'Fetched matches data from GitHub (length: {len(matches_data)})')

# # determine the paths to get the necessary data from lineups and events
# lineups_paths = []
# events_paths = []
# for match in matches_data:
#     match_id = match['match_id']
#     lineups_paths.append(f'lineups/{match_id}.json')
#     events_paths.append(f'events/{match_id}.json')

# # get the lineups data
# lineups_data = get_json_data_from_paths(lineups_paths)
# print(f'Fetched lineups data from GitHub (length: {len(lineups_data)})')

# # get the events data
# events_data = get_json_data_from_paths(events_paths)
# print(f'Fetched events data from GitHub (length: {len(events_data)})')

# TESTING ADDING AND CONNECTING TO THE POSTGRESQL DB -------------------------

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
    
'''

# CREATE TABLE IF NOT EXISTS managers (
#         id INT PRIMARY KEY,
#         name VARCHAR(255),
        
#     );

# CREATE TABLE IF NOT EXISTS teams (
#         team_id INT PRIMARY KEY,
#         team_name VARCHAR(255),
#         team_gender VARCHAR(255),
#         team_group VARCHAR(255),
#         country_name VARCHAR(255),
#         manager_id INT,
#         FOREIGN KEY (manager_id) REFERENCES managers (manager_id)
#     );

# CREATE TABLE IF NOT EXISTS matches (
#         match_id INT PRIMARY KEY,
#         match_date DATE,
#         kick_off TIME,
#         competition_id INT,
#         season_id INT,
#         FOREIGN KEY (competition_id) REFERENCES competitions (competition_id),
#         FOREIGN KEY (season_id) REFERENCES seasons (season_id)
#     );

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
    INSERT INTO COMPETITIONS (competition_id, season_id, country_name,
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
        WHERE competition_id = %s
    );
'''

cur = conn.cursor() # a cursor object to execute SQL commands

cur.execute(CREATE_TABLES_QUERY) # execute the CREATE TABLE statement
conn.commit() # commit the transaction

# prepare and execute the INSERT statement for each item in valid_comp_data
for comp in valid_comp_data:
    # populate the seasons table
    season_id = comp['season_id']
    seasons_values = (season_id, comp['season_name'], season_id)
    cur.execute(INSERT_SEASONS_QUERY, seasons_values)

    # populate the competitions table
    comp_id = comp['competition_id']
    comp_values = (comp_id, comp['season_id'], comp['country_name'],
                   comp['competition_name'], comp['competition_gender'],
                   comp['competition_youth'],
                   comp['competition_international'], comp['season_name'],
                   comp_id)
    cur.execute(INSERT_COMPS_QUERY, comp_values)

print('Populated the seasons table.')
print('Populated the competitions table.')

for match in matches_data:
    print(match)
    print()

conn.commit() # commit the transaction

# close the cursor and connection
cur.close()
conn.close()