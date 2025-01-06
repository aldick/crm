from django.utils import timezone
from django.db import models
from django.urls import reverse
import datetime

from clients.models import Client, Worker

class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name="Имя товара")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Количество", default=0)
    sell_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость при продаже")
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Себестоимость")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to="products/", verbose_name="Изображение")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("products_detail", args=[self.id])
    
class Combo(models.Model):
    products = models.ManyToManyField(Product, through='ProductsInCombo', verbose_name="Продукты")
    name = models.CharField(max_length=50, verbose_name="Имя товара")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to="products/", verbose_name="Изображение")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость")
    discount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Скидка")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("combo_detail", args=[self.id])
    
class ProductsInCombo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    combo = models.ForeignKey(Combo, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Количество")
    
    def __str__(self):
        return f'{self.combo.name}     {self.product.name}'
    
    
class Supply(models.Model):
    product = models.ForeignKey(Product,
                                related_name="supplies",
                                on_delete=models.CASCADE,
                                verbose_name="Продукт")
    worker = models.ForeignKey(Worker,
                               related_name="supplies",
                               on_delete=models.CASCADE,
                               verbose_name="Рабочий")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Количество")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
