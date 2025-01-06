from orders.models import Order, OrderItem
from storage.models import Product
from clients.models import Client

from random import randrange, randint, choice
from datetime import timedelta, datetime

def random_date():
	start = datetime(2025, 1, 1)
	end = datetime(2025, 2, 1)
	delta = end - start
	int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
	random_second = randrange(int_delta)
	return start + timedelta(seconds=random_second)

streets_file = open('static/txt/streets.txt', 'r') 
streets = []
for street in streets_file:
    streets.append(street[:-1])

clients = Client.objects.all()
clients_list = [client.phone_number for client in clients]

products = Product.objects.all()
products_list = [product.name for product in products]

for i in range(300):
	phone_number = choice(clients_list)
	address = choice(streets) + " " + str(randint(1, 1000))
	stage = randint(1, 4)
	type_of_payment = randint(1, 3)
	type_of_order = randint(1, 2)
	created_at = random_date()
	order = Order(
    	phone_number_id=int(phone_number),
     	address=address,stage=stage,
      	type_of_payment=type_of_payment,
       	type_of_order=type_of_order,
        created_at=created_at
    )
	order.save()
	for j in range(randint(1, 5)):
		product_name = choice(products_list)
		product = Product.objects.get(name=product_name)
		amount = randint(1, 3)
		order_item = OrderItem(order_id=order.id, product_id=product.id, amount=amount)
		order_item.save()


orders = Order.objects.all()
for order in orders:
    client = Client.objects.get(phone_number=order.phone_number)
    client.total += order.get_total_cost()
    client.save()