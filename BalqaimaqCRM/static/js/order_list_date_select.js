document.addEventListener('DOMContentLoaded', (event) => {
	let url = window.location.href
	let position = url.search("date")
	let date = url[position+5]
	
	switch(date) {
		case 't':
			document.getElementById("select").selectedIndex = "0";
			break;
		case 'y':
			document.getElementById("select").selectedIndex = "1";
			break;
		case 'w':
			document.getElementById("select").selectedIndex = "2";
			break;
		case 'm':
			document.getElementById("select").selectedIndex = "3";
			break;
	}

	document.getElementById('select').addEventListener('change', function() {
		console.log('You selected: ', this.value);
		window.location.href = '?date=' + this.value
	});
})
