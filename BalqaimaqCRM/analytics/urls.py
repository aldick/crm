from django.urls import path
from . import views

urlpatterns = [
	path('get-selling/<slug:date>', views.get_selling, name="get_selling"),
	path('selling/', views.selling_view, name="analytics_selling"),
	
	path('get-products/<slug:date>', views.get_products, name="get_products"),	
	path('products/', views.products_view, name="analytics_products"),
]
