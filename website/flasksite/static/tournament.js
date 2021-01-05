
fetch('./api/tournament')
  	.then(response => response.json())
  	.then(data => buildTournament(data))


buildTournament = function (data) {
	data = data['data']

	gridContainer = document.querySelector('#tournament')

	for (let round in data) {
		for (let bracket in data[round]) {
			bracketDiv = document.createElement('div')
			if (data[round][bracket][0] == null) {data[round][bracket][0] = "?"}
			if (data[round][bracket][1] == null) {data[round][bracket][1] = "?"}
			bracketDiv.innerHTML = data[round][bracket][0] + " vs " + data[round][bracket][1]
			bracketDiv.classList.add('bracket')
			bracketDiv.classList.add('bordered')
			roundpp = parseInt(round) + 1
			bracketpp = parseInt(bracket) + 1
			bracketDiv.style['grid-area'] = "b" + roundpp.toString() + bracketpp.toString()
			gridContainer.appendChild(bracketDiv)
		}
	}
}