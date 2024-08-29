from django.urls import path

from . import views

urlpatterns = [
	path('', views.products_list_view, name="products_list"),
	path('<int:pk>/', views.products_detail_view, name="products_detail"),
	path('create/', views.products_create_view, name="products_create"),
	path('update/<int:pk>/', views.products_update_view, name="products_update"),
	path('supply/', views.products_supply_view, name="products_supply")
]
