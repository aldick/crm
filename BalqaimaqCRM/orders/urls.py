from django.urls import path, re_path

from . import views


urlpatterns = [
	path("", views.orders_list_view, name="orders_list"),
]
