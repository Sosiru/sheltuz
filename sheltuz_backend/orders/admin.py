from django.contrib import admin

from orders.models import Cart, Wishlist, Order, OrderItem


# Register your models here.
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
	"""
	Seller model admin. Defines the fields to display and which ones are searchable
	"""

	list_filter = ('customer', 'product_qty', 'product__name', 'state__name', 'date_created', 'date_modified')
	list_display = ('product', 'product_qty', 'customer', 'state', 'date_created', 'date_modified')
	search_fields = ('product__name', 'product_qty', 'state__name', 'date_created', 'date_modified')
	order_by = ('customer__name', 'product_qty', 'product__name', 'state__name', 'date_created', 'date_modified')


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
	"""
	Seller model admin. Defines the fields to display and which ones are searchable
	"""
	list_filter = ('customer', 'product__name', 'state__name', 'date_created', 'date_modified')
	list_display = ('product', 'customer', 'state', 'date_created', 'date_modified')
	search_fields = ('product__name', 'state__name', 'date_created', 'date_modified')
	order_by = ('customer__name', 'product__name', 'state__name', 'date_created', 'date_modified')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	"""
	Order model admin. Defines the fields to display and which ones are searchable
	"""
	list_filter = ('buyer', 'phone', 'total_price', 'status', 'paid', 'tracking_number', 'state', 'date_created', 'date_modified')
	list_display = ('buyer', 'phone', 'total_price', 'status', 'paid', 'tracking_number', 'state', 'date_created', 'date_modified')
	search_fields = ('buyer__name', 'phone', 'total_price', 'status', 'paid', 'tracking_number', 'paid', 'tracking_number', 'state__name', 'date_created', 'date_modified')
	order_by = ('buyer', 'phone', 'total_price', 'status', 'paid', 'tracking_number', 'state', 'date_created', 'date_modified')


@admin.register(OrderItem)
class OrderAdmin(admin.ModelAdmin):
	"""
	Order model admin. Defines the fields to display and which ones are searchable
	"""
	list_filter = ('order__buyer', 'product', 'product_cost', 'product_qty', 'date_created', 'date_modified')
	list_display = ('product', 'product_cost', 'product_qty', 'state')
	search_fields = ('order__buyer', 'product__name', 'product_cost', 'product_qty', 'state__name')
	order_by = ('order__buyer', 'product', 'product_cost', 'product_qty', 'date_created', 'date_modified')