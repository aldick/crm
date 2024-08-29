#Launched in python manage.py shell
import random

from .models import Client

names_file = open('/home/aldick/Programming/BalqaimaqCRM/BalqaimaqCRM/clients/static/txt/names.txt', 'r')
names = []
for name in names_file:
    names.append(name[:-1])
names_file.close()

phone_number_starts = ['777', '707', '700', '705', '787', '771', '775']

streets_file = open('/home/aldick/Programming/BalqaimaqCRM/BalqaimaqCRM/clients/static/txt/streets.txt', 'r') 
streets = []
for street in streets_file:
    streets.append(street[:-1])

for name in names:
    phone_number = '+7' + random.choice(phone_number_starts) + str(random.randint(1000000, 10000000))
    address = random.choice(streets) + " " + str(random.randint(1, 1000))
    
    client = Client(phone_number=phone_number, name=name, address=address) 
    client.save()
    