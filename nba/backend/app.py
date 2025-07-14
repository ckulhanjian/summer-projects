import json
from flask import Flask, render_template, request, jsonify
# from shot_graph import generate_shot_graph
from heatmap import generate_heatmap

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_players", methods=["GET"])
def get_players():
    with open("rosters/2024-25-nba_roster.json", "r") as f:
        data = json.load(f)

        '''
        making a dictionary of team names to list of players
        '''    
        teams_data = {}
        for player in data:
            team = player["TEAM_NAME"]
            name = player["PLAYER"]
            if team not in teams_data:
                teams_data[team] = [name]
            else:
                teams_data[team].append(name)

    return jsonify(teams_data)

@app.route("/generate_graph", methods=["POST"])
def generate_graph():
    data = request.get_json()
    player_name = data.get("player")

    if not player_name:
        return jsonify({"error": "Player name is required"}), 400
    
    # Call the function from player_graph.py to generate the graph and get the image path
    image_path = generate_heatmap(player_name)
    
    # Return the path of the image for use in the frontend
    return jsonify({"graph_url": f"/{image_path}"})

if __name__ == "__main__":
    app.run(debug=True)