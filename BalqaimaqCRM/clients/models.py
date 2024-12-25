from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Client(models.Model):
    phone_number = models.CharField(verbose_name="Номер телефона", max_length=11, unique=True, primary_key=True)
    password = models.CharField(verbose_name="Пароль", max_length=100, default="12345678")
    name = models.CharField(verbose_name="Имя", max_length=100)
    address = models.CharField(verbose_name="Адрес", max_length=150)
    total = models.DecimalField(verbose_name="Общая сумма заказов", default=0, max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.phone_number
    
class Worker(Client):
    pass