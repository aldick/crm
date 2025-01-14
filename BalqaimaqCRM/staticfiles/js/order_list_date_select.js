let params = new URLSearchParams(document.location.search);
let date = params.get('date');
let month = params.get('month');
let year = params.get('year');

function addScript(src){
	var script = document.createElement('script');
	script.src = src;
	script.async = false; // чтобы гарантировать порядок
	document.head.appendChild(script);
}

function date_select() {
	console.log(month, year, date)
	if(month == null && year == null && date == null) {
		date = 't';
	}
	switch(date) {
		case 't':
			return 0
			break;
		case 'y':
			return 1
			break;
		case 'cw':
			return 2
			break;
		case 'pw':
			return 3
			break;
		case 'cm':
			return 4
			break;
		case 'pm':
			return 5
			break;
		default:
			let select = document.getElementById("select");
			let opt = document.createElement('option');

			opt.value = '';
			opt.innerHTML = `${month}-ый месяц, ${year}`;
			select.appendChild(opt);

			return 7
			break;
	}
}

function loader(index) {
	// Показываем анимацию загрузки
	// document.getElementById('loader').style.display = 'block';
	// Делаем AJAX запрос с помощью fetch

	let query = ''
	if(index == 7) query = `?month=${month}&year=${year}`
	else query = `?date=${date}`
	console.log(`/get-orders/${query}`)
	fetch(`/orders/get-orders/${query}`)
		.then(response => response.json())
		.then(data => {
			console.log(data)
			for(let i=1; i<5; i++) {
				let final_cost = 0
				for(order in data[i]) {
					order = data[i][order]
					final_cost += order['total_cost']
					document.getElementById(`tasks${i}`).insertAdjacentHTML(
						'beforeend',
						`
							<div class="task ${order['id']}" draggable="true" data-price="${order['total_cost']}">
								<div>
									<button ondblclick="window.location='${order['url']['orders_detail_url']}'" class="board-item-content-text id" href="${order['url']['orders_detail_url']}">Заказ #${order['id']}</button>
									<br>
									<button ondblclick="window.location='${order['url']['clients_detail_url']}'" class="board-item-content-text phone_number" href="${order['url']['clients_detail_url']}">
										Номер телефона: +${order['phone_number']}
									</button>
									<p class="board-item-content-text created_at">
										Дата заказа: ${order['date']}
									</p>
									<p class="board-item-content-text address">
										Время: ${order['time']}
									</p>
									<p class="board-item-content-text address">
										Адрес: ${order['address']}
									</p>
									<b data-price="{{order.get_total_cost}}" class="board-item-content-text price">
										${order['total_cost']} ₸
									</b>
								</div>
							</div>	
						`
					)
				}
				document.getElementById(`title${i}`).insertAdjacentHTML(
					'afterend',
					`<h3>${ final_cost } ₸</h3>`
				)

			}
			
			addScript("../static/js/drag&drop.js");

			document.getElementById('loader').style.display = 'none';
			document.getElementById('content').style.display = 'block';
		})
		.catch(error => {
			console.log(error)
			document.getElementById('loader').textContent = 'Ошибка загрузки';
		});
}

document.addEventListener('DOMContentLoaded', (event) => {
	let index = date_select()
	document.getElementById('select').selectedIndex = index;

	loader(index)

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
