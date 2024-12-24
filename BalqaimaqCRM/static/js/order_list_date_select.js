//TODO добавить больше выбора
document.addEventListener('DOMContentLoaded', (event) => {
	let url = window.location.href
	let position = url.search("date")
	let date = url[position+5]
	if (url[position+6]) {
		date = url[position+5] + url[position+6]
	}
	console.log(date)
	
	switch(date) {
		case 't':
			document.getElementById("select").selectedIndex = "0";
			break;
		case 'y':
			document.getElementById("select").selectedIndex = "1";
			break;
		case 'cw':
			document.getElementById("select").selectedIndex = "2";
			break;
		case 'pw':
			document.getElementById("select").selectedIndex = "3";
			break;
		case 'cm':
			document.getElementById("select").selectedIndex = "4";
			break;
		case 'pm':
			document.getElementById("select").selectedIndex = "5";
			break;
	}

	document.getElementById('select').addEventListener('change', function() {
		console.log('You selected: ', this.value);
		window.location.href = '?date=' + this.value
	});
})
