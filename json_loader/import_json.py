import requests

VALID_SEASONS = {
    'La Liga': ['2018/2019', '2019/2020', '2020/2021'],
    'Premier League': ['2003/2004']
}

def import_json_from_github(path : str) -> list:
    url = f'https://raw.githubusercontent.com/statsbomb/open-data/0067cae/data/{path}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Failed to fetch {path}: {response.status_code}')
        return

def get_json_data_from_paths(paths : str) -> list:
    data = []
    for path in paths:
        json_data = import_json_from_github(path)
        if json_data:
            data.extend(json_data)
        else:
            print(f'Failed to fetch {path} from GitHub.')
    return data

# get the necessary data from competitions.json and store it in valid_comp_data
comp_data = get_json_data_from_paths(['competitions.json'])
print(f'Fetched competitions data from GitHub (length: {len(comp_data)})')
valid_comp_data = []
for comp in comp_data:
    comp_name = comp['competition_name']
    if comp_name in VALID_SEASONS.keys() and comp['season_name'] in VALID_SEASONS[comp_name]:
        valid_comp_data.append(comp)
print(f'Fetched valid competitions data from GitHub (length: {len(valid_comp_data)})')

# determine the paths to get the necessary data from matches
matches_paths = []
for comp in valid_comp_data:
    comp_id = comp['competition_id']
    season_id = comp['season_id']
    matches_paths.append(f'matches/{comp_id}/{season_id}.json')

# get the necessary data from matches and store it in valid_matches_data
matches_data = get_json_data_from_paths(matches_paths)
print(f'Fetched matches data from GitHub (length: {len(matches_data)})')

# determine the paths to get the necessary data from lineups and events
lineups_paths = []
events_paths = []
for match in matches_data:
    match_id = match['match_id']
    lineups_paths.append(f'lineups/{match_id}.json')
    events_paths.append(f'events/{match_id}.json')

# get the necesssary data from lineups and store it in valid_lineups_data
lineups_data = get_json_data_from_paths(lineups_paths)
print(f'Fetched lineups data from GitHub (length: {len(lineups_data)})')

# get the necessary data from events and store it in valid_events_data
events_data = get_json_data_from_paths(events_paths)
print(f'Fetched events data from GitHub (length: {len(events_data)})')
