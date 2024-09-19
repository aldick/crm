let myChart;
let Jsondata;

let ctx = document.getElementById('myChart');

var options = {
	method: 'GET',
	mode: 'same-origin',
}

fetch(`../get-orders/week/`, options)
.then(function(response){
	if(response.status == 200){
		return response.json();
	}
})
.then(function(data){ 
	JsonData = data;
	createChart(JsonData, 'bar');
	console.log(data)
});	

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
		fetch(`../get-orders/${this.value}/`, options)
		.then(function(response){
			if(response.status == 200){
				return response.json();
			}
		})
		.then(function(data){ 
			JsonData = data;
			createChart(JsonData, 'bar');
			console.log(data)
		});	
	});
})



function createChart(data, type){
	let labels = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
	let values = []
	for (var key in data) {
		values.push(data[key])
		console.log( "Ключ: " + key + " значение: " + data[key] );
	}
	if (myChart) {
		myChart.destroy();
	}
	myChart = new Chart(ctx, {
	   // Setting the chart's type to the `type` parameter.
	   type: type, 
	   data: {
		  labels: labels, 
		  
		  datasets: [{
			 label: '# of Income',
			 
			 data: values,
			 
			 borderWidth: 1
		 }]
	   },
	   options: {
		  scales: {
			 y: {
				beginAtZero: true
			 }
		  },
		  // Making the chart responsive.
		  responsive: true,
		  maintainAspectRatio: false,
	   }
	});
 }
