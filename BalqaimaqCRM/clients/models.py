from django.db import models


class Client(models.Model):
    phone_number = models.CharField(max_length=15)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)