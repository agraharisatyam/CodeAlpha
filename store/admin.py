from django.contrib import admin

from .models import Order, OrderItem, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__username", "email", "full_name")
    inlines = [OrderItemInline]

# Register your models here.
