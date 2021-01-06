
url = document.querySelector('#url').innerHTML

game_data = {}
fetch('/blolleyball/api/replays/' + url)
  	.then(response => response.json())
  	.then(data => game_data = data['data'])
  	.then(data => render_replay(game_data))

let urlParams = new URLSearchParams(window.location.search);
if (urlParams.has('t')) {
	current_step = urlParams.get('t')
}
else {
	current_step = 0
}

playing = false

play_next = function () {
	if (playing) {
		if (current_step >= game_data.length) {
			play()
		}
		else {
		current_step += 1
		}
		render_replay(game_data)
		setTimeout(play_next, 3000)
	}
}

backToStart = function () {
	current_step = 0
	render_replay(game_data)
}

backFast = function () {
	current_step = Math.max(current_step - 10, 0)
	render_replay(game_data)
}

back = function () {
	current_step = Math.max(current_step - 1, 0)
	render_replay(game_data)
}

play = function () {
	playing = !playing
	let playButton = document.querySelector('#play')
	if (playing) {
		playButton.innerHTML = '⏸️'
		play_next()
	}
	else {
		playButton.innerHTML = '▶️'
	}
}

forward = function () {
	current_step = Math.min(current_step + 1, game_data.length - 1)
	render_replay(game_data)
}

forwardFast = function () {
	current_step = Math.min(current_step + 10, game_data.length - 1)
	render_replay(game_data)
}

forwardToEnd = function () {
	current_step = game_data.length - 1
	render_replay(game_data)
}

share = function () {
  shareField = document.querySelector('#share-field')
  shareField.style.display = 'block'
  shareField.select()
  document.execCommand('copy')
  shareField.style.display = 'none'
  shareText = document.querySelector('#share-text')
  shareText.innerHTML = 'Copied to Clipboard'
  setTimeout(shareBack, 1000)
}

shareBack = function () {
  shareText = document.querySelector('#share-text')
  shareText.innerHTML = 'Share'
}

render_replay = function (data) {
	d = data[current_step]
	let events = d.events
    let stats = d.stats
    let field = d.field
    let touches = d.touches
    let set_score = d.set_score
    let score = d.score
    let teams = d.teams

    let progressCurrent = document.querySelector('#progress-current')
    progressCurrent.innerHTML = current_step

    let progressEnd = document.querySelector('#progress-end')
    progressEnd.innerHTML = data.length

    let titleDiv = document.querySelector("#title")
    titleDiv.innerHTML = "Blolleyball - " + teams[0] + " vs " + teams[1]

    let fieldDiv = document.querySelector("#field-text")
    fieldDiv.innerHTML = field

    let setScoreDiv = document.querySelector("#score-game")
    setScoreDiv.innerHTML = set_score[0] + " - " + set_score[1]

    let curSetDiv = document.querySelector("#score-current")
    let setCount = set_score[0] + set_score[1] + 1

    if (score.length > 0) {
    	curSetDiv.innerHTML = "Set " + setCount + ": <br>" + score[setCount-1][0] + " - " + score[setCount-1][1]
	}
	else {
		curSetDiv.innerHTML = "Game Start"
	}

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

    let shareField = document.querySelector('#share-field')
    url = window.location.href
    url = url.split('?')[0]
    url += '?t=' + current_step
    shareField.value = url
}