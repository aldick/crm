from django.urls import path, re_path

from . import views


urlpatterns = [
	path("", views.orders_list_view, name="orders_list"),
	path("detail/<int:order_id>/", views.orders_detail_view, name="orders_detail"),
	path("create/<int:phone_number>", views.orders_create_view, name="orders_create"),
	path("update/<int:order_id>/", views.orders_update_view, name="orders_update"),
	path("delete/<int:order_id>/", views.orders_delete_view, name="orders_delete"),

	path("item-delete/<int:item_id>/", views.orders_item_delete_view, name="orders_item_delete"),
	path("column-update/<int:order_id>/<slug:order_stage>/", views.orders_column_update_view, name="orders_column_update"),
]
