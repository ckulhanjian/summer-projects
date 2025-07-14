
let teamsData = {};

// Fetch the team/player data "get me some data"
async function loadTeams() {
    const response = await fetch('/get_players');
    teamsData = await response.json(); // javascript object

    const teamSelect = document.getElementById("team-select"); // select object
    teamSelect.innerHTML = "";  // Clear first

     // 🔽 Add default option
    const defaultOption = document.createElement("option");
    defaultOption.value = "";
    defaultOption.textContent = "-- Select a Team --";
    defaultOption.disabled = true;
    defaultOption.selected = true;
    teamSelect.appendChild(defaultOption);

    for (const team in teamsData) { // every team name
        const option = document.createElement("option"); // new option element for dropdown
        option.value = team; // set value of option
        option.textContent = team; // visible text
        teamSelect.appendChild(option); // <option value="Miami Heat">Miami Heat</option>
    }

    // Load players for the first team
    // updatePlayerDropdown(teamSelect.value);
    // teamSelect.value is the current selected team
    // updatePlayerDropdown populates the players when team is chosen

    // Update players when team changes: event listener
    teamSelect.addEventListener("change", () => {
        updatePlayerDropdown(teamSelect.value);
    });
}

// Populate players based on selected team
function updatePlayerDropdown(team) {
    const playerSelect = document.getElementById("player-select");
    playerSelect.innerHTML = "";

    // 🔽 Add default option
    const defaultOption = document.createElement("option");
    defaultOption.value = "";
    defaultOption.textContent = "-- Select a Player --";
    defaultOption.disabled = true;
    defaultOption.selected = true;
    playerSelect.appendChild(defaultOption);

    for (const player of teamsData[team]) {
        const option = document.createElement("option");
        option.value = player;
        option.textContent = player;
        playerSelect.appendChild(option);
    }
}

// Handle graph generation
// "here is some data, do something with it"
document.getElementById("generate-button").addEventListener("click", async () => {
    const player = document.getElementById("player-select").value; // name
    const response = await fetch("/generate_graph", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ player })
    });

    const data = await response.json();
    document.getElementById("graph-image").src = data.graph_url + "?v=" + new Date().getTime(); // force reload
});

// On load
loadTeams();