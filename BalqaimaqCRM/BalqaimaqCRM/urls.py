from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from orders.views import orders_list_view


urlpatterns = [
    path('', orders_list_view),
    path('admin/', admin.site.urls),
    path('clients/', include('clients.urls')),
    path('storage/', include('storage.urls')),
    path('orders/', include('orders.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
