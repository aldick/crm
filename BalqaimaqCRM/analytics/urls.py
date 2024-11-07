from django.urls import path
from . import views

urlpatterns = [
	path('get-selling/<slug:date>', views.get_selling, name="get_selling"),
	path('get-types-of-orders/<slug:date>', views.get_types_of_orders, name="get_types_of_orders"),
	path('get-types-of-payments/<slug:date>', views.get_types_of_payments, name="get_types_of_payments"),
	path('selling/', views.selling_view, name="analytics_selling"),
	
	path('get-products/<slug:date>', views.get_products, name="get_products"),	
	path('products/', views.products_view, name="analytics_products"),
 
	path('workers/', views.workers_view, name="analytics_workers"),
]
