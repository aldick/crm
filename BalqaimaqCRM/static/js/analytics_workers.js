document.addEventListener('DOMContentLoaded', (event) => {
	let url = window.location.href
	
	let position = url.search("date")
	let date = url[position+5] + url[position+6]
	if (date == ':/') date = "cw";
	switch(date) {
		case 'cw': // current week
			document.getElementById("select").selectedIndex = "0";
			break;
		case 'pw': // previous week 
			document.getElementById("select").selectedIndex = "1";
			break;
		case 'cm': // current month
			document.getElementById("select").selectedIndex = "2";
			break;
		case 'pm': // previous month
 			document.getElementById("select").selectedIndex = "3";
			break;
	}

	document.getElementById('select').addEventListener('change', function() {
		// console.log('You selected: ', this.value);
		window.location.href = '?date=' + this.value
	});
})
