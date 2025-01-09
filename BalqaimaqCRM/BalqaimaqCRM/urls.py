from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from orders.views import orders_list_view
from clients.views import clients_login_view, clients_logout_view

urlpatterns = [
    path('', orders_list_view),
    path('login/', clients_login_view, name='login'),
    path('logout/', clients_logout_view, name='logout'),
    path('admin/', admin.site.urls),
    path('clients/', include('clients.urls')),
    path('storage/', include('storage.urls')),
    path('orders/', include('orders.urls')),
    path('analytics/', include('analytics.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
