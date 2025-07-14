import json
from flask import Flask, render_template, jsonify
# from shot_graph import generate_shot_graph

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

@app.route("/generate-graph", methods=["POST"])
def generate_graph():
    return

if __name__ == "__main__":
    app.run(debug=True)