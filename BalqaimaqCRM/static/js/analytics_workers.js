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
	
	var options = {
		method: 'GET',
		mode: 'same-origin',
	}

	let phone_number = document.getElementById('phone-number').innerHTML.slice(1)

	fetch(`../../analytics/get-workers-supplies/${phone_number}/${date}`, options)
	.then(function(response){
		if(response.status == 200){
			return response.json();
		}
	})
	.then(function(data){ 
		JsonData = data;
		createChart(JsonData, date[1]);
	});	

	document.getElementById('select').addEventListener('change', function() {
		window.location.href = '?date=' + this.value
	});
})


function createChart(data, date){
	let ctx = document.getElementById('myChart');
	let labels = []
	let values = []
	
	if (date == 'w') {
		labels = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
	} else {
		for (let i=1; i<data.days+1; i++) {
			labels.push(i)
		}
	}

	let datasets = []
	let colors = ['#00FFFF', '#5F9EA0', '#7FFFD4', '#1E90FF', '#00008B', '#8B008B', '#6A5ACD', '#DDA0DD', "#FF00FF", "#D2691E", "#8B4513", "#D2B48C", '#FFA500', '#FF6347', '#8B0000', '#FF0000', '#FFA07A', '#00FF00', '#98FB98', '#00FA9A', '#3CB371', '#DAA520', '#228B22', '#9ACD32', '#66CDAA', '#20B2AA', '#ADFF2F', '#7FFF00']
	let counter = 0
	for (product in data.supplies) {
		let dataset = {
			label: product,
			data: data.supplies[product],
			backgroundColor: colors[counter],
		}
		counter++;
		datasets.push(dataset)
	}

	myChart = new Chart(ctx, {
		type: 'bar', 
		data: {
			labels: labels, 
			
			datasets: datasets,
		},
		options: {
			scales: {
				y: {
				  beginAtZero: true,
				  stacked: true,
				},
  
			 	x: {
				  	stacked: true,
			  	}
		  	},
			responsive: true,
			maintainAspectRatio: false,
	   	}
	});
}