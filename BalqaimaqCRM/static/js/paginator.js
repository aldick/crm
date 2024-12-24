document.addEventListener('DOMContentLoaded', (event) => {
	var page = 1;
	var emptyPage = false;
	var blockRequest = false;

	const searchParams = new URLSearchParams(window.location.search);

	window.addEventListener('scroll', function(e) {
		var margin = document.body.clientHeight - window.innerHeight - 200;
		if(window.pageYOffset > margin && !emptyPage && !blockRequest) {
			blockRequest = true;
			page += 1;
			console.log(page)
			
			if(!searchParams.has('phone_number')) {
				fetch(`?phone_number=${phone_number}&clients_only=1&page=`+page)
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
		}
	});

	const scrollEvent = new Event('scroll');
	window.dispatchEvent(scrollEvent);
})