from django.contrib import admin

from payments.models import PaymentTransaction


# Register your models here.
@admin.register(PaymentTransaction)
class CartAdmin(admin.ModelAdmin):
	"""
	Seller model admin. Defines the fields to display and which ones are searchable
	"""

	list_filter = ('phone_number', 'checkout_request_id', 'amount', 'status', 'ip','date_created', 'date_modified')
	list_display = ('phone_number', 'checkout_request_id', 'amount', 'status', 'ip','date_created', 'date_modified')
	search_fields = ('phone_number', 'checkout_request_id', 'amount', 'status', 'ip','date_created', 'date_modified')
	order_by = ( 'phone_number', 'checkout_request_id', 'amount', 'status', 'ip','date_created', 'date_modified')