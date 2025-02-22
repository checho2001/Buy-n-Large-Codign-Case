from django.contrib import admin

# Register your models here.

from .models import Product, Order


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')
    search_fields = ('name', 'description')
    list_filter = ('category', 'brand')

admin.site.register(Product, ProductAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'status', 'total_price', 'created_at')
    search_fields = ('user__username', 'product__name')
    list_filter = ('created_at',)

admin.site.register(Order, OrderAdmin)


