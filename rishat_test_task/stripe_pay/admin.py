from django.contrib import admin

from .models import Discount, Item, Order, Tax


class DiscountInline(admin.TabularInline):
    model = Order.discounts.through


class TaxInline(admin.TabularInline):
    model = Order.taxes.through


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name', 'price', 'currency',)
    list_editable = ('name',)
    list_filter = ('name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields = ('id',)
    list_display = ('id', 'has_discount',)
    inlines = (DiscountInline, TaxInline)


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    search_fields = ('amount',)
    list_display = ('id', 'amount',)
    list_editable = ('amount',)
    list_filter = ('amount',)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    search_fields = ('amount',)
    list_display = ('id', 'amount',)
    list_editable = ('amount',)
    list_filter = ('amount',)
