from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.static import players
import seaborn as sns
# import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use the non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc
# import uuid
import os

# Ensure the directory exists
if not os.path.exists('static/graphs'):
    os.makedirs('static/graphs')

# Function to get player shot data
def get_player_shots(id, season):
    response = shotchartdetail.ShotChartDetail(
        team_id=0,               # 0 means just the player
        player_id=id,
        season_type_all_star='Regular Season',  # or 'Playoffs', etc.
        season_nullable=season,
        context_measure_simple='FGA'  # Field Goal Attempts
    )
    df = response.get_data_frames()[0]
    df['X'] = (df['LOC_X'] / 12).round(2)
    df['Y'] = (df['LOC_Y'] / 12).round(2)
    data = df[['X', 'Y']]  # Ensure these columns exist
    return data

# Function to plot the density heatmap of shots
def plot_density(data, color='plasma'):
    fig, ax = plt.subplots(figsize=(5, 5))  # taller for vertical layout
    sns.kdeplot(
        x=data['X'],
        y=data['Y'],
        fill=True,
        cmap=color,
        bw_adjust=1,  # smooth v sharp 1 = smooth & blurry
        thresh=0.01,  # Minimum density threshold (5%) (too empty v too full - adjust)
        levels=200,  # Number of gradient levels
        ax=ax
    )
    return fig, ax

# Function to draw the basketball court lines
def draw_half_court(ax, color='black', lw=2):
    hoop_y = 4  # hoop is 4 ft in from baseline
    paint_height = 19
    free_throw_line_y = paint_height
    free_throw_circle_radius = 6
    three_point_radius = 23.75
    corner_three_height = 16.75  # side line height
    corner_three_dist = 22  # feet from center (NBA rules: 22 ft from corner)
    arc_start_x = 14  # arc starts curving 3 ft from sideline (court width is 50 ft)

    # Hoop and backboard
    hoop = Circle((0, hoop_y), radius=0.75, linewidth=lw, color=color, fill=False)
    backboard = Rectangle((-3, hoop_y - 0.1), 6, 0.1, linewidth=lw, color=color)

    baseline = Rectangle((-25, 0), 50, 0.1, linewidth=lw, color=color)

    # Paint rectangles
    outer_box = Rectangle((-8, 0), 16, paint_height, linewidth=lw, color=color, fill=False)
    inner_box = Rectangle((-6, 0), 12, paint_height, linewidth=lw, color=color, fill=False)

    # Free throw circle (top half)
    ft_circle = Arc((0, free_throw_line_y), 12, 12, theta1=0, theta2=180, linewidth=lw, color=color)

    # Restricted area arc
    restricted = Arc((0, hoop_y), 8, 8, theta1=0, theta2=180, linewidth=lw, color=color)

    # 3-point arc (top half only)
    arc = Arc((0, 4), 50.8, 50.8, theta1=30, theta2=150, linewidth=lw, color=color)

    # Side 3-point lines (vertical from baseline to corner_three_height)
    side_line_left = Rectangle((-corner_three_dist, 0), 0.01, corner_three_height,linewidth=lw, color=color)
    side_line_right = Rectangle((corner_three_dist, 0), 0.01, corner_three_height, linewidth=lw,color=color)

    for element in [hoop, backboard, outer_box, inner_box, ft_circle,
                    restricted, arc, side_line_left, side_line_right, baseline]:
        ax.add_patch(element)

    # Setup plot
    ax.set_xlim(-25, 25)
    ax.set_ylim(0, 47)
    ax.set_aspect('equal')

# Function to adjust the appearance of the plot
def features(ax):
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.set_yticks(range(0, 41, 10))
    ax.tick_params(axis='y', labelsize=7)
    ax.get_xaxis().set_visible(False)
    ax.set_ylabel('Distance from Baseline')
    ax.tick_params(axis='x', labelsize=7)

def generate_heatmap(player_name, direction=1):
    season = '2024-25'
    player_data = players.find_players_by_full_name(player_name)[0]
    player_id = player_data['id']

    # Get shot data and generate heatmap
    data = get_player_shots(player_id, season)
    data['Y'] = data['Y'] + 4  # adjust for hoop distance

    fig, ax = plot_density(data, color="coolwarm")
    draw_half_court(ax)
    if direction == 1:
        ax.invert_yaxis()
    features(ax)
    
    # Save image with player's name
    filename = f"static/graphs/{player_name.replace(' ', '_')}.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    
    return filename

# Example usage
'''
image_path = main(player_name)  # You can pass any player name here
'''
