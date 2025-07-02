from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.static import players
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc

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

def plot_density(data, color='plasma'):
    
    fig, ax = plt.subplots(figsize=(5, 5))  # taller for vertical layout
    sns.kdeplot(
        x=data['X'],
        y=data['Y'],
        fill=True,
        cmap=color,
        bw_adjust=1, # smooth v sharp 1 = smooth & blurried
        thresh=0.01,  # Minimum density threshold to show color (5%) (too emoty v too fill - adjust)
        levels=200, # Number of gradient levels (detail in color)
        ax=ax
        ) # this makes the plot
    return fig, ax

def draw_half_court(ax, color='black', lw=2):
    # Coordinates: baseline at y=0, court extends upward to 47 ft

    # --- Base measurements ---
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

def features(ax):
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.set_yticks(range(0, 41, 10))  # You can include 47 this way
    ax.tick_params(axis='y', labelsize=7)
    ax.get_xaxis().set_visible(False)
    ax.set_ylabel('Distance from Baseline')
    ax.tick_params(axis='x', labelsize=7)

def display_player(season, player, direction):
    # basic info
    id1 = player['id']
    data1 = get_player_shots(id1,season)
    # adjust for hoop distance from baseline
    data1['Y'] = data1['Y']+4
    # plot heatmap
    fig, ax = plot_density(data1, color="coolwarm")
    # draw court lines
    draw_half_court(ax)
    # special features
    if direction==1:
        ax.invert_yaxis()
    features(ax)
    return plt

def main():
        season = '2024-25'
        player1 = players.find_players_by_full_name("Bam Adebayo")[0]
        # player name & id
        display_player(season, player1, 1)
        plt.savefig(f"players/{player1['first_name']}{player1['last_name']}.png", dpi=300, bbox_inches='tight')
        # {'id': 1628389, 'full_name': 'Bam Adebayo', 'first_name': 'Bam', 'last_name': 'Adebayo', 'is_active': True}
main()