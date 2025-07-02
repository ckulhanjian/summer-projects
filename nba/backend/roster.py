# imports
import time
import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonteamroster

# 1. choose season
season = '2024-25'

# 2. store rosters & missing info (not fetched)
total_roster = [] # list of dataframes
missing_teams = []

# 3. get team rosters
for team in teams.get_teams(): # all teams
    name = team['full_name'] # team name
    id = team['id'] # team id
    try:
        print(f"Fetching {name} data")
        roster = commonteamroster.CommonTeamRoster(team_id=id, season='2023-24') # team roster
        df = roster.get_data_frames()[0][['PLAYER', 'PLAYER_ID']] # player name & ID
        # add team name & id
        df['TEAM_NAME'] = name 
        df['TEAM_ID'] = id
        total_roster.append(df) # add 
        time.sleep(3)  
    except Exception as e:
        print(f"Failed to fetch {name}: {e}")
        missing_teams.append((name,id))


# 4. retry for missing teams
for name, id in missing_teams:
    try:
        time.sleep(3)
        print(f"Fetching {name} data")
        roster = commonteamroster.CommonTeamRoster(team_id=id, season='2023-24')
        df = roster.get_data_frames()[0][['PLAYER', 'PLAYER_ID']]
        df['TEAM_NAME'] = name
        df['TEAM_ID'] = id
        total_roster.append(df)
    except Exception as e:
        print(f"Still failed: {name}")

# 5. combine list of data frames into one (stacks vertically & reset index))
# 6. store roster in json
if total_roster:
    final_roster = pd.concat(total_roster, ignore_index=True)
    final_roster.to_json(f"{season}-nba_roster.json", orient="records", indent=2)
else:
    print("No team rosters were successfully fetched.")
