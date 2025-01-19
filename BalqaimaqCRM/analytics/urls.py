from django.urls import path
from . import views

urlpatterns = [
	path('get-selling/<slug:date>', views.get_selling, name="get_selling"),
	path('get-types-of-orders/<slug:date>', views.get_types_of_orders, name="get_types_of_orders"),
	path('get-types-of-payments/<slug:date>', views.get_types_of_payments, name="get_types_of_payments"),
	path('selling/', views.selling_view, name="analytics_selling"),
	
	path('get-products/<slug:date>', views.get_products, name="get_products"),	
	path('products/', views.products_view, name="analytics_products"),
 
	path('get-workers-supplies/<slug:phone_number>/<slug:date>', views.get_workers_supplies, name="get_workers_supplies"),
	path('workers-list/', views.workers_list_view, name="analytics_workers_list"),
	path('workers-detail/<slug:phone_number>', views.workers_detail_view, name="analytics_workers_detail"),
	path('workers-create/', views.workers_create_view, name="analytics_workers_create"),
	path('workers-update/<slug:phone_number>/', views.workers_update_view, name="analytics_workers_update"),
	path('workers-delete/<slug:phone_number>/', views.workers_delete_view, name="analytics_workers_delete"),
]
