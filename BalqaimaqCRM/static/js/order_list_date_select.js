function date_select() {
	let params = new URLSearchParams(document.location.search);
	let date = params.get('date');
	let month = params.get('month');
	let year = params.get('year');
	console.log(month, year, date)
	if(month == null && year == null && date == null) {
		date = 't';
	}
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
		default:
			let select = document.getElementById("select");
			let opt = document.createElement('option');

			opt.value = '';
			opt.innerHTML = `${month}-ый месяц, ${year}`;
			select.appendChild(opt);

			document.getElementById("select").selectedIndex = "7";
			break;
	}
}

document.addEventListener('DOMContentLoaded', (event) => {
	date_select()

	const modal = document.querySelector(".date-select");

	document.getElementById('select').addEventListener('change', function() {
		console.log('You selected: ', this.value);
		if(this.value!='mine') {
			window.location.href = '?date=' + this.value
		} else {
			modal.showModal();
		}
	});

	// confirm deletion
	modal.addEventListener("submit", () => currentTask && currentTask.remove());

	// cancel deletion
	modal.querySelector("#cancel").addEventListener("click", function() {
		modal.close();
		date_select()
	})
})
