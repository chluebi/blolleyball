
let socket = new WebSocket("ws://chluebi.com/websockets");

socket.onmessage = function(event) {
  d = JSON.parse(event.data)
  console.log("[message] Data received from server:");

  parse_data(d)
};

parse_data = function(d) {
  if (d.event == "match") {
    let events = d.events
    let stats = d.stats
    let field = d.field
    let touches = d.touches
    let set_score = d.set_score
    let score = d.score
    let teams = d.teams

    let titleDiv = document.querySelector("#title")
    titleDiv.innerHTML = "Blolleyball - " + teams[0] + " vs " + teams[1]

    let fieldDiv = document.querySelector("#field-text")
    fieldDiv.innerHTML = field

    let setScoreDiv = document.querySelector("#score-game")
    setScoreDiv.innerHTML = set_score[0] + " - " + set_score[1]

    let curSetDiv = document.querySelector("#score-current")
    let setCount = set_score[0] + set_score[1] + 1
    curSetDiv.innerHTML = "Set " + setCount + ": <br>" + score[setCount-1][0] + " - " + score[setCount-1][1]

    for (let i=1; i<score.length+1; i++) {
      let setDiv = document.querySelector("#set" + i)
      setDiv.innerHTML = "Set " + i + ": " + score[i-1][0] + " - " + score[i-1][1]
    }

    let touchesDiv = document.querySelector("#touches")
    touchesDiv.innerHTML = "Touches: " + touches

    let eventDiv = document.querySelector("#event")
    eventDiv.innerHTML = ""
    for (let event of events) {
      eventDiv.innerHTML += event + "<br>"
    }

    let statDiv = document.querySelector("#stats")
    if (stats.length < 1) {
      statDiv.hidden = true;
    }
    else {
      statDiv.hidden = false;
      statDiv.innerHTML = stats
    }
  }
  if (event == "over") {
    let titleDiv = document.querySelector("#title")
    titleDiv.innerHTML += "Match is over"
  }
}

socket.onclose = function(event) {
  if (event.wasClean) {
    console.log("[close] Connection closed cleanly, code=${event.code} reason=${event.reason}");
  } else {
    // e.g. server process killed or network down
    // event.code is usually 1006 in this case
    console.log("[close] Connection died");
    let titleDiv = document.querySelector("#title")
    titleDiv.innerHTML = "No Match playing"
  }
};

socket.onerror = function(error) {
  console.log("[error] ${error.message}");
};

let test_data = {"event": "match", "events": ["Set #1: 0-1", "Gamers"], "stats": "", "field": "   _ _ _ _   _ _ _ _\n  |        |        |\n  | 3   4  |  6   1 |\n  |        |        |\n  | 2   5  |  5   2 |  \n  |        |        |\n  | 1   6  |  4   3 |\n  |_ _ _ _ |_ _ _ _ |", "touches": 0, "set_score": [0, 0], "score": [[0, 1]], "teams": ["Karasuno", "Nekoma"]}
console.log(test_data)
parse_data(test_data)