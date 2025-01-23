document.addEventListener('DOMContentLoaded', (event) => {
	let url = window.location.href
	
	let position = url.search("date")
	let date = url[position+5] + url[position+6]
	if (date == ':/' || date == "s:") date = "cw";
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

	fetch(`../get-selling/${date}`, options)
	.then(function(response){
		if(response.status == 200){
			return response.json();
		}
	})
	.then(function(data){ 
		JsonData = data;
		createChart(JsonData, 'bar', date[1]);
		total_sum = document.getElementById('total-sum');
		total_sum.innerHTML = JsonData.total_sum;
	});	

	fetch(`../get-types-of-orders/${date}`, options)
	.then(function(response){
		if(response.status == 200){
			return response.json();
		}
	})
	.then(function(data){ 
		JsonData = data;
		createPieChart(document.getElementById('myChart2'), data);
	});	

	fetch(`../get-types-of-payments/${date}`, options)
	.then(function(response){
		if(response.status == 200){
			return response.json();
		}
	})
	.then(function(data){ 
		JsonData = data;
		createPieChart(document.getElementById('myChart3'), data);
	});	

	document.getElementById('select').addEventListener('change', function() {
		window.location.href = '?date=' + this.value
	});
})

function createChart(data, type, date){
	let ctx = document.getElementById('myChart1');
	let labels = []
	let values = []
	
	if (date == 'w') {
		labels = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
		for (var key in data.days) {
			values.push(data["days"][key])
		}
	} else {
		for (var key in data.days) {
			labels.push(key)
			values.push(data["days"][key])
		}
	}

	myChart = new Chart(ctx, {
	   // Setting the chart's type to the `type` parameter.
	   type: type, 
	   data: {
		  labels: labels, 
		  
		  datasets: [{
			 label: 'Заказов',
			 
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

function createPieChart(ctx, data) {
	let labels = []
	let values = []
	for (var key in data) {
		labels.push(key)
		values.push(data[key])
	}

	ctx = new Chart(ctx, {
		// Setting the chart's type to the `type` parameter.
		type: 'pie', 
		data: {
		   labels: labels, 
		   
		   datasets: [{
			  label: 'Заказов',
			  
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