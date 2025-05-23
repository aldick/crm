#Launched in python manage.py shell
import random

from clients.models import Client

names_file = open('static/txt/names_ru.txt', 'r')
names = []
for name in names_file:
    names.append(name[:-1].capitalize())
names_file.close()

phone_number_starts = ['777', '707', '700', '705', '787', '771', '775']

streets_file = open('static/txt/streets.txt', 'r') 
streets = []
for street in streets_file:
    streets.append(street[:-1])

for name in names:
    phone_number = '7' + random.choice(phone_number_starts) + str(random.randint(1000000, 10000000))
    address = random.choice(streets) + " " + str(random.randint(1, 1000))
    
    client = Client(phone_number=phone_number,  name=name, address=address) 
    client.save()
    