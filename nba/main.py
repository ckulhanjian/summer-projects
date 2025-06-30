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
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc

id = 1628389
season = '2024-25'

def get_player_shots(id, season):
    response = shotchartdetail.ShotChartDetail(
        team_id=0,               # use 0 if you're just interested in the player
        player_id=id,
        season_type_all_star='Regular Season',  # also options: 'Playoffs', etc.
        season_nullable=season,
        context_measure_simple='FGA'  # Field Goal Attempts
    )

    df = response.get_data_frames()[0]
    df['X'] = (df['LOC_X'] / 12).round(2)
    df['Y'] = (df['LOC_Y'] / 12).round(2)
    data = df[['X', 'Y']]  # Make sure these exist
    return data

# Plot shot frequency density heatmap
def plot_density(data, color='coolwarm'):
    plt.figure(figsize=(10, 8))
    sns.kdeplot(
        x=data['X'],
        y=data['Y'],
        cmap=color,
        bw_adjust=1, # smooth v sharp 1 = smooth & blurried
        thresh=0.00,  # Minimum density threshold to show color (5%) (too emoty v too fill - adjust)
        levels=100 # Number of gradient levels (detail in color)
    ) # this makes the plot
    # Set labels
    plt.title("Shot Chart Heatmap")
    # gca gets current axses - after plotting...its where plot lives
    plt.gca().invert_yaxis() # Flip the y-axis (so basket is on top) 
    ax = plt.gca() 
    ax.xaxis.tick_top() # Move x-axis label and ticks to the top
    # Clean up axis limits
    plt.axis('equal')
    plt.xlim(-25, 25)
    plt.show()

def draw_half_court(ax=None, color='black', lw=2):
    if ax is None:
        ax = plt.gca()
    # Hoop
    hoop = Circle((0, 0), radius=0.75, linewidth=lw, color=color, fill=False)
    # Backboard
    backboard = Rectangle((-3, -0.75), 6, 0.1, linewidth=lw, color=color)
    # Paint (key)
    outer_box = Rectangle((-8, -0.75), 16, 19, linewidth=lw, color=color, fill=False)
    inner_box = Rectangle((-6, -0.75), 12, 19, linewidth=lw, color=color, fill=False)
    # Free throw arc
    top_arc = Arc((0, 19), 12, 12, theta1=0, theta2=180, linewidth=lw, color=color)
    # Restricted zone
    restricted = Arc((0, 0), 8, 8, theta1=0, theta2=180, linewidth=lw, color=color)
    # Three-point line
    corner_three_left = Rectangle((-22, -0.75), 0.1, 14, linewidth=lw, color=color)
    corner_three_right = Rectangle((22, -0.75), 0.1, 14, linewidth=lw, color=color)
    three_arc = Arc((0, 0), 47.5, 47.5, theta1=22, theta2=158, linewidth=lw, color=color)
    # Add all elements to the plot
    court_elements = [hoop, backboard, outer_box, inner_box, top_arc,
                      restricted, corner_three_left, corner_three_right, three_arc]
    for element in court_elements:
        ax.add_patch(element)
    return ax

# draw_half_court(ax)
id = 1628389
season = '2024-25'
plot_density(get_player_shots(id,season))
