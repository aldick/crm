from django.db import models


class Client(models.Model):
    phone_number = models.CharField(verbose_name="Номер телефона", max_length=15)
    name = models.CharField(verbose_name="Имя", max_length=100)
    address = models.CharField(verbose_name="Адрес", max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.phone_number
    