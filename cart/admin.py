from django.contrib import admin
from .models import Item


# Register your models here.
class ItemAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "price", "quantity")


admin.site.register(Item, ItemAdmin)
