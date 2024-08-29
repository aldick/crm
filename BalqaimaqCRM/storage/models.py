from django.db import models
from django.urls import reverse

from clients.models import Client


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name="Имя товара")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Количество", default=0)
    sell_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость при продаже")
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Себестоимость")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to="products/", verbose_name="Изображение")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("products_detail", args=[self.id])

class Supply(models.Model):
    product = models.ForeignKey(Product,
                                related_name="supplies",
                                on_delete=models.CASCADE,
                                verbose_name="Продукт")
    worker = models.ForeignKey(Client,
                               related_name="supplies",
                               on_delete=models.CASCADE,
                               verbose_name="Рабочий")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Количество")
    
