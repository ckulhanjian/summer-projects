'''
1. user will choose 2 players
2. on each player
    - get shot map
    - generate heap map
'''

{
    "PLAYER":"Bam Adebayo",
    "PLAYER_ID":1628389,
    "TEAM_NAME":"Miami Heat",
    "TEAM_ID":1610612748
}

from nba_api.stats.endpoints import shotchartdetail

id = 1628389
season = '2024-25'

response = shotchartdetail.ShotChartDetail(
    team_id=0,               # use 0 if you're just interested in the player
    player_id=id,
    season_type_all_star='Regular Season',  # also options: 'Playoffs', etc.
    season_nullable=season,
    context_measure_simple='FGA'  # Field Goal Attempts
)

df = response.get_data_frames()[0]

print(df)
