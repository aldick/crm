from django.urls import path

from . import views

urlpatterns = [
	path('', views.products_list_view, name="products_list"),
	path('table/<slug:slug>/', views.products_table_view, name="products_table_order_by"),
	path('table', views.products_table_view, name="products_table"),
	path('<int:pk>/', views.products_detail_view, name="products_detail"),
	path('create/', views.products_create_view, name="products_create"),
	path('update/<int:pk>/', views.products_update_view, name="products_update"),
	path('delete/<int:pk>/', views.products_delete_view, name="products_delete"),
	path('supply/', views.products_supply_view, name="products_supply"),
 
	path('combo/<int:pk>/', views.combo_detail_view, name="combo_detail"),
	path('combo/create/', views.combo_create_view, name="combo_create"),
	path('combo/update/<int:pk>/', views.combo_update_view, name='combo_update'),
	path('combo/delete/<int:pk>/', views.combo_delete_view, name='combo_delete'),
]
