from django.urls import path
from . import views


urlpatterns = [
	path('', views.clients_list_view, name="clients_list"),
	path('<int:pk>/', views.clients_detail_view, name="clients_detail"),
	path('order_by/<slug:slug>/', views.clients_list_order_view, name="clients_list_order_by"),
	path('create/', views.clients_create_view, name="clients_create"),
	path('update/<int:pk>', views.clients_update_view, name="clients_update"),
]
