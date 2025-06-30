from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.static import players
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc
import base64
from io import BytesIO

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
    data = df[['X', 'Y']]  
    return data

def plot_density(data1, data2, color='plasma'):
    fig, ax = plt.subplots(figsize=(8, 8))  
    sns.kdeplot(
        x=data1['X'],
        y=data1['Y'],
        fill=True,
        cmap='Blues',
        bw_adjust=1, 
        thresh=0.01,  
        levels=200, 
        ax=ax
        ) 
    sns.kdeplot(
        x = -(data2['X']),
        y = 94-data2['Y'],
        fill=True,
        cmap='Reds',
        bw_adjust=1, 
        thresh=0.01,  
        levels=200, 
        ax=ax
        ) 
    return fig, ax

def draw_bottom_half(ax, color='white', lw=2):
    hoop = Circle((0, 0), radius=0.75, linewidth=lw, color=color, fill=False)
    backboard = Rectangle((-3, -0.75), 6, 0.1, linewidth=lw, color=color)
    outer_box = Rectangle((-8, -0.75), 16, 19, linewidth=lw, color=color, fill=False)
    inner_box = Rectangle((-6, -0.75), 12, 19, linewidth=lw, color=color, fill=False)
    restricted = Arc((0, 0), 8, 8, theta1=0, theta2=180, linewidth=lw, color=color)
    three_arc = Arc((0, 0), 47.5, 47.5, theta1=0, theta2=180, linewidth=lw, color=color)

    for element in [hoop, backboard, outer_box, inner_box, restricted, three_arc]:
        ax.add_patch(element)

def draw_top_half(ax, color='white', lw=2):
    base_y = 94  
    hoop = Circle((0, base_y), radius=0.75, linewidth=lw, color=color, fill=False)
    backboard = Rectangle((-3, base_y + 0.75), 6, -0.1, linewidth=lw, color=color)
    outer_box = Rectangle((-8, base_y + 0.75), 16, -19, linewidth=lw, color=color, fill=False)
    inner_box = Rectangle((-6, base_y + 0.75), 12, -19, linewidth=lw, color=color, fill=False)
    restricted = Arc((0, base_y), 8, 8, theta1=180, theta2=360, linewidth=lw, color=color)
    three_arc = Arc((0, base_y), 47.5, 47.5, theta1=180, theta2=360, linewidth=lw, color=color)

    for element in [hoop, backboard, outer_box, inner_box, restricted, three_arc]:
        ax.add_patch(element)

def draw_full_court(ax, color='white', lw=2):
    draw_bottom_half(ax, color=color, lw=lw) 
    draw_top_half(ax, color=color, lw=lw) 
    return ax

def create_interactive_html(fig, player1_name, player2_name, season):
    """Convert matplotlib figure to interactive HTML"""
    
    # Convert figure to base64 string
    buffer = BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight', 
                facecolor='black', dpi=200, transparent=False)
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode()
    buffer.close()
    
    # Create HTML with embedded image and interactive buttons
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NBA Shot Heatmap: {player1_name} vs {player2_name}</title>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                background: linear-gradient(135deg, #1a1a2e, #16213e);
                color: white;
                margin: 0;
                padding: 20px;
                min-height: 100vh;
            }}
            .container {{
                max-width: 1000px;
                margin: 0 auto;
                background: rgba(255, 255, 255, 0.1);
                padding: 30px;
                border-radius: 15px;
                backdrop-filter: blur(10px);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            }}
            .header {{
                text-align: center;
                margin-bottom: 30px;
            }}
            .title {{
                font-size: 2.5em;
                margin-bottom: 10px;
                background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }}
            .subtitle {{
                font-size: 1.2em;
                color: #ccc;
                margin-bottom: 20px;
            }}
            .player-info {{
                display: flex;
                justify-content: space-around;
                margin-bottom: 20px;
            }}
            .player-card {{
                background: rgba(255, 255, 255, 0.1);
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                min-width: 200px;
            }}
            .player-blue {{
                border-left: 4px solid #3498db;
            }}
            .player-red {{
                border-left: 4px solid #e74c3c;
            }}
            .controls {{
                text-align: center;
                margin-bottom: 30px;
            }}
            .btn {{
                background: linear-gradient(45deg, #667eea, #764ba2);
                border: none;
                color: white;
                padding: 12px 24px;
                margin: 5px;
                cursor: pointer;
                border-radius: 25px;
                font-size: 14px;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            }}
            .btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
            }}
            .btn-info {{
                background: linear-gradient(45deg, #3498db, #2980b9);
            }}
            .btn-download {{
                background: linear-gradient(45deg, #e74c3c, #c0392b);
            }}
            .btn-reset {{
                background: linear-gradient(45deg, #95a5a6, #7f8c8d);
            }}
            .image-container {{
                text-align: center;
                position: relative;
                margin-bottom: 30px;
            }}
            #heatmap-image {{
                max-width: 100%;
                height: auto;
                border-radius: 10px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
                transition: all 0.3s ease;
            }}
            .legend {{
                display: flex;
                justify-content: center;
                gap: 30px;
                margin-top: 20px;
            }}
            .legend-item {{
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            .legend-color {{
                width: 20px;
                height: 20px;
                border-radius: 3px;
            }}
            .blue-legend {{
                background: linear-gradient(45deg, #3498db, #2980b9);
            }}
            .red-legend {{
                background: linear-gradient(45deg, #e74c3c, #c0392b);
            }}
            .info-panel {{
                background: rgba(255, 255, 255, 0.1);
                padding: 20px;
                border-radius: 10px;
                margin-top: 20px;
                display: none;
            }}
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-top: 15px;
            }}
            .stat-card {{
                background: rgba(255, 255, 255, 0.1);
                padding: 15px;
                border-radius: 8px;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1 class="title">NBA Shot Heatmap Analysis</h1>
                <p class="subtitle">Season: {season}</p>
            </div>
            
            <div class="player-info">
                <div class="player-card player-blue">
                    <h3>{player1_name}</h3>
                    <p>Blue Heatmap</p>
                </div>
                <div class="player-card player-red">
                    <h3>{player2_name}</h3>
                    <p>Red Heatmap</p>
                </div>
            </div>
            
            <div class="controls">
                <button class="btn btn-info" onclick="showAnalysis()">📊 Show Analysis</button>
                <button class="btn btn-info" onclick="showLegend()">📋 Show Legend</button>
                <button class="btn btn-download" onclick="downloadImage()">💾 Download Image</button>
                <button class="btn btn-reset" onclick="resetView()">🔄 Reset View</button>
            </div>
            
            <div class="image-container">
                <img id="heatmap-image" src="data:image/png;base64,{image_base64}" alt="NBA Shot Heatmap">
            </div>
            
            <div class="legend">
                <div class="legend-item">
                    <div class="legend-color blue-legend"></div>
                    <span>{player1_name} Shot Density</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color red-legend"></div>
                    <span>{player2_name} Shot Density</span>
                </div>
            </div>
            
            <div id="info-panel" class="info-panel">
                <h3>Analysis</h3>
                <div id="info-content">
                    Click a button above to see detailed analysis.
                </div>
            </div>
        </div>

        <script>
            function showAnalysis() {{
                const panel = document.getElementById('info-panel');
                const content = document.getElementById('info-content');
                
                content.innerHTML = `
                    <h4>Shot Heatmap Analysis</h4>
                    <div class="stats-grid">
                        <div class="stat-card">
                            <strong>Blue Areas ({player1_name})</strong><br>
                            Higher concentration of shot attempts<br>
                            Warmer colors = More shots taken
                        </div>
                        <div class="stat-card">
                            <strong>Red Areas ({player2_name})</strong><br>
                            Shot attempts from opposite court perspective<br>
                            Shows complementary shooting patterns
                        </div>
                        <div class="stat-card">
                            <strong>Court Layout</strong><br>
                            Full NBA court (94ft x 50ft)<br>
                            Three-point arcs and key areas marked
                        </div>
                        <div class="stat-card">
                            <strong>Data Source</strong><br>
                            NBA API - {season} Regular Season<br>
                            Real shooting location data
                        </div>
                    </div>
                `;
                
                panel.style.display = 'block';
            }}
            
            function showLegend() {{
                const panel = document.getElementById('info-panel');
                const content = document.getElementById('info-content');
                
                content.innerHTML = `
                    <h4>How to Read This Heatmap</h4>
                    <p><strong>Density Colors:</strong></p>
                    <ul>
                        <li><strong>Darker/Cooler colors:</strong> Fewer shot attempts from that location</li>
                        <li><strong>Brighter/Warmer colors:</strong> More shot attempts from that location</li>
                        <li><strong>Blue heatmap:</strong> {player1_name}'s shooting patterns</li>
                        <li><strong>Red heatmap:</strong> {player2_name}'s shooting patterns (mirrored)</li>
                    </ul>
                    <p><strong>Court Elements:</strong></p>
                    <ul>
                        <li>Three-point arcs at both ends</li>
                        <li>Free throw lanes and circles</li>
                        <li>Restricted areas under baskets</li>
                        <li>Court dimensions: 94ft length × 50ft width</li>
                    </ul>
                `;
                
                panel.style.display = 'block';
            }}
            
            function downloadImage() {{
                const link = document.createElement('a');
                link.href = 'data:image/png;base64,{image_base64}';
                link.download = '{player1_name}_{player2_name}_shot_heatmap_{season}.png';
                link.click();
                
                // Show confirmation
                const btn = event.target;
                const originalText = btn.innerHTML;
                btn.innerHTML = '✅ Downloaded!';
                btn.style.background = '#27ae60';
                setTimeout(() => {{
                    btn.innerHTML = originalText;
                    btn.style.background = 'linear-gradient(45deg, #e74c3c, #c0392b)';
                }}, 2000);
            }}
            
            function resetView() {{
                const panel = document.getElementById('info-panel');
                const img = document.getElementById('heatmap-image');
                
                panel.style.display = 'none';
                img.style.filter = 'none';
                img.style.transform = 'scale(1)';
            }}
            
            // Add some interactive effects
            document.getElementById('heatmap-image').addEventListener('click', function() {{
                this.style.transform = this.style.transform === 'scale(1.1)' ? 'scale(1)' : 'scale(1.1)';
            }});
        </script>
    </body>
    </html>
    """
    
    return html_content

def main():
    # Get player data
    player1 = players.find_players_by_full_name("Bam Adebayo")[0]
    player2 = players.find_players_by_full_name("Duncan Robinson")[0]
    id1 = player1['id']
    id2 = player2['id']
    name1 = player1['full_name']
    name2 = player2['full_name']
    season = '2024-25'
    
    # Get shot data
    print("Fetching shot data...")
    data1 = get_player_shots(id1, season)
    data2 = get_player_shots(id2, season)
    
    # Create the plot
    print("Creating heatmap...")
    fig, ax = plot_density(data1, data2, "coolwarm")
    
    # Draw court elements
    draw_full_court(ax, color='white', lw=2)
    
    # Styling
    ax.set_facecolor('black')
    ax.plot([-25, 25], [47, 47], color='white', linewidth=2)
    ax.text(0, 37, f"{name1}", fontsize=12, ha='center', color='white', weight='bold')
    ax.text(0, 57, f"{name2}", fontsize=12, ha='center', color='white', weight='bold')
    ax.set_xlim(-25, 25)
    ax.set_ylim(0, 94)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.title(f"Shot Heatmap: {name1} vs {name2} ({season})", 
              fontsize=16, color='white', pad=20)
    plt.tight_layout()
    
    # Create HTML
    print("Generating HTML...")
    html_output = create_interactive_html(fig, name1, name2, season)
    
    # Save HTML file
    filename = f'nba_heatmap_{name1.replace(" ", "_")}_{name2.replace(" ", "_")}.html'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_output)
    
    print(f"✅ Interactive HTML saved as: {filename}")
    print("🌐 Open this file in your web browser to view the interactive heatmap!")
    
    # Optionally still show the matplotlib plot
    plt.show()
    
    plt.close(fig)

if __name__ == "__main__":
    main()