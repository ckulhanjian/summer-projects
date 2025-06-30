
{
    "PLAYER":"Bam Adebayo",
    "PLAYER_ID":1628389,
    "TEAM_NAME":"Miami Heat",
    "TEAM_ID":1610612748
}

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

# Plot shot frequency density heatmap
def plot_density(data1, data2, color='plasma'):
    fig, ax = plt.subplots(figsize=(4, 4))  # taller for vertical layout
    sns.kdeplot(
        x=data1['X'],
        y=data1['Y'],
        fill=True,
        cmap='Blues',
        bw_adjust=1, # smooth v sharp 1 = smooth & blurried
        thresh=0.01,  # Minimum density threshold to show color (5%) (too emoty v too fill - adjust)
        levels=200, # Number of gradient levels (detail in color)
        # alpha=0.8,
        ax=ax
        ) # this makes the plot
    sns.kdeplot(
        x = -(data2['X']),
        y = 94-data2['Y'],
        fill=True,
        cmap='Reds',
        bw_adjust=1, # smooth v sharp 1 = smooth & blurried
        thresh=0.01,  # Minimum density threshold to show color (5%) (too emoty v too fill - adjust)
        levels=200, # Number of gradient levels (detail in color)
        # alpha=0.8,
        ax=ax
        ) # this makes the plot
    return ax

def draw_bottom_half(ax, color='black', lw=2):
    # Origin at y = 0, court faces UP (standard)
    hoop = Circle((0, 0), radius=0.75, linewidth=lw, color=color, fill=False)
    backboard = Rectangle((-3, -0.75), 6, 0.1, linewidth=lw, color=color)
    outer_box = Rectangle((-8, -0.75), 16, 19, linewidth=lw, color=color, fill=False)
    inner_box = Rectangle((-6, -0.75), 12, 19, linewidth=lw, color=color, fill=False)
    restricted = Arc((0, 0), 8, 8, theta1=0, theta2=180, linewidth=lw, color=color)
    three_arc = Arc((0, 0), 47.5, 47.5, theta1=0, theta2=180, linewidth=lw, color=color)

    for element in [hoop, backboard, outer_box, inner_box, restricted, three_arc]:
        ax.add_patch(element)

def draw_top_half(ax, color='black', lw=2):
    # Origin at y = 94, court faces DOWN
    base_y = 94  # flip around this line
    hoop = Circle((0, base_y), radius=0.75, linewidth=lw, color=color, fill=False)
    backboard = Rectangle((-3, base_y + 0.75), 6, -0.1, linewidth=lw, color=color)
    outer_box = Rectangle((-8, base_y + 0.75), 16, -19, linewidth=lw, color=color, fill=False)
    inner_box = Rectangle((-6, base_y + 0.75), 12, -19, linewidth=lw, color=color, fill=False)
    restricted = Arc((0, base_y), 8, 8, theta1=180, theta2=360, linewidth=lw, color=color)
    three_arc = Arc((0, base_y), 47.5, 47.5, theta1=180, theta2=360, linewidth=lw, color=color)

    for element in [hoop, backboard, outer_box, inner_box, restricted, three_arc]:
        ax.add_patch(element)

def draw_full_court(ax, color='black', lw=2):
    draw_bottom_half(ax, color=color, lw=lw) # Bottom half (0 to 47 feet)
    draw_top_half(ax, color=color, lw=lw) # Top half (47 to 94 feet)
    return ax

def draw_plot(ax, player1, player2):
    ax.set_facecolor('black')
    ax.plot([-25, 25], [47, 47], color='black', linewidth=2)
    ax.text(0, 37 , f"{player1}", fontsize=10, ha='center')
    ax.text(0, 57 , f"{player2}", fontsize=10, ha='center')
    ax.set_xlim(-25, 25)
    ax.set_ylim(0, 94)  # full court
    ax.set_aspect('equal')
    ax.axis('off')
    plt.title("Shot Heatmap + Court", fontsize=16)
    plt.tight_layout()
    plt.show()

def main():
    player1 = players.find_players_by_full_name("Bam Adebayo")[0]
    player2 = players.find_players_by_full_name("Duncan Robinson")[0]
    id1 = player1['id']
    id2 = player2['id']
    name1 = player1['full_name']
    name2 = player2['full_name']
    season = '2024-25'
    data1 = get_player_shots(id1,season)
    data2 = get_player_shots(id2,season)
    ax = plot_density(data1, data2,"coolwarm")
    draw_full_court(ax)
    draw_plot(ax, name1, name2)


main()