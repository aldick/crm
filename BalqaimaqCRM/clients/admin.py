from django.contrib import admin
from .models import Client, Worker

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass

@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    pass