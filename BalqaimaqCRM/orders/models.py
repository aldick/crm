from django.db import models

from clients.models import Client
from storage.models import Product

class Order(models.Model):
    STAGES = {"1": 'Упаковка', 
              "2": 'Готов к доставке', 
              "3": "Доставляется", 
              "4": "Завершен"}
    TYPE_OF_PAYMENTS = {"1": 'Kaspi QR', 
                        "2": 'Перевод', 
                        "3": "Наличные"}
    TYPE_OF_ORDERS = {"1": "Онлайн", 
                      "2": "Оффлайн"}
    
    phone_number = models.ForeignKey(Client,
                                     related_name="orders",
                                     on_delete=models.CASCADE)
    # name = models.CharField(verbose_name="Имя", max_length=100)
    address = models.CharField(verbose_name="Адрес", max_length=150)
    stage = models.CharField(verbose_name="Этап заказа", choices=STAGES, max_length=20, default="1")
    type_of_payment = models.CharField(verbose_name="Тип оплаты", choices=TYPE_OF_PAYMENTS, max_length=20)
    type_of_order = models.CharField(verbose_name="Тип заказа", choices=TYPE_OF_ORDERS, max_length=20)
    review = models.TextField(verbose_name="Отзыв клиента", max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
			models.Index(fields=['-created_at']),
		]
        
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def __str__(self):
        return f'Order {self.id}'
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order,
							related_name='items',
							on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name="order_items",
                                on_delete=models.CASCADE,
                                verbose_name="Продукт")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Количество")
    
    def __str__(self):
	    return str(self.id)
 
    def get_cost(self):
        return round(self.product.sell_price * self.amount)
	
	