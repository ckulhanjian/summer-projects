import plotly.graph_objects as go
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.static import players
import pandas as pd
import plotly.io as pio

def get_player_shots(id, season):
    response = shotchartdetail.ShotChartDetail(
        team_id=0,
        player_id=id,
        season_type_all_star='Regular Season',
        season_nullable=season,
        context_measure_simple='FGA'
    )
    df = response.get_data_frames()[0]
    df['X'] = (df['LOC_X'] / 12).round(2)
    df['Y'] = (df['LOC_Y'] / 12).round(2)
    data = df[['X', 'Y']]  # Make sure these exist
    return data

def plot_shot_comparison(data1, data2, player1, player2, season='2024-25'):
    fig = go.Figure()

    # Player 1 Heatmap (bottom)
    fig.add_trace(go.Histogram2dContour(
        x=data1['X'], y=data1['Y'],
        colorscale='Blues', opacity=0.6,
        contours=dict(showlines=False),
        showscale=False, name=player1
    ))

    # Player 2 Heatmap (top)
    fig.add_trace(go.Histogram2dContour(
        x=data2['X'], y=data2['Y'],
        colorscale='Reds', opacity=0.6,
        contours=dict(showlines=False),
        showscale=False, name=player2
    ))

    return fig

def draw_court(fig, p1, p2):
    # Half court line
    fig.add_shape(type="line",
                  x0=-25, y0=47, x1=25, y1=47,
                  line=dict(color="black", width=2))

    # Labels
    fig.add_annotation(x=0, y=37, text=p1, showarrow=False, font=dict(size=14))
    fig.add_annotation(x=0, y=57, text=p2, showarrow=False, font=dict(size=14))

    # Layout
    fig.update_layout(
        title=f"Shot Chart Comparison: {p1} vs {p2}",
        xaxis=dict(range=[-25, 25], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[0, 94], showgrid=False, zeroline=False, visible=False),
        width=600, height=1000,
        paper_bgcolor='white',
        plot_bgcolor='white',
        showlegend=False
    )

def add_full_court_to_plotly(fig, lw=2, color='black'):

    fig.update_layout(shapes=shapes)


def main():
    player1 = "Bam Adebayo"
    player2 = "Duncan Robinson"
    season = "2024-25"

    id1 = players.find_players_by_full_name(player1)[0]['id']
    id2 = players.find_players_by_full_name(player2)[0]['id']

    data1 = get_player_shots(id1, season)
    data2 = get_player_shots(id2, season)

    data2['X'] = -data2['X']
    data2['Y'] = 94 - data2['Y']

    fig = plot_shot_comparison(data1, data2, player1, player2, season)
    draw_court(fig,player1,player2)
    add_full_court_to_plotly(fig)

    pio.write_html(fig, "shot_chart.html", auto_open=True)


main()