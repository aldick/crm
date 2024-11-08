document.addEventListener('DOMContentLoaded', (event) => {
	var page = 1;
	var emptyPage = false;
	var blockRequest = false;

	window.addEventListener('scroll', function(e) {
		var margin = document.body.clientHeight - window.innerHeight - 200;
		if(window.pageYOffset > margin && !emptyPage && !blockRequest) {
			blockRequest = true;
			page += 1;
			console.log(page)
			
			
			fetch('?clients_only=1&page='+page)
			.then(response => response.text())
			.then(html => {
				if (html === '') {
					emptyPage = true;
				}
				else {
					var imageList = document.getElementById('table');
					imageList.insertAdjacentHTML('beforeEnd', html);
					blockRequest = false;
				}
			})
		}
	});

	const scrollEvent = new Event('scroll');
	window.dispatchEvent(scrollEvent);
})