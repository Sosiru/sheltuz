from django.contrib import admin

from base.models import State, AccountFieldType, PaymentMethod, Country, Transaction, TransactionType


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
	"""
	State model admin. Defines the fields to display and which ones are searchable
	"""
	list_filter = ('date_created',)
	list_display = ('name', 'description', 'date_modified', 'date_created')
	search_fields = ('name',)


@admin.register(AccountFieldType)
class AccountTypeAdmin(admin.ModelAdmin):
	"""
	AccountFieldType model admin. Defines the fields to display and which ones are searchable
	"""
	list_filter = ('date_created',)
	list_display = ('name', 'description', 'state', 'date_modified', 'date_created')
	search_fields = ('name', 'state__name')


# @admin.register(Destination)
# class DestinationAdmin(admin.ModelAdmin):
# 	"""
# 	Destination model admin. Defines the fields to display and which ones are searchable
# 	"""
# 	list_filter = ('date_created',)
# 	list_display = ('name', 'description', 'state', 'date_modified', 'date_created')
# 	search_fields = ('name', 'state__name')


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
	"""
	EntryChannel model admin. Defines the fields to display and which ones are searchable
	"""
	list_filter = ('date_created',)
	list_display = ('name', 'description', 'state', 'date_modified', 'date_created')
	search_fields = ('name', 'state__name')


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
	"""
	Country model admin. Defines the fields to display and which ones are searchable
	"""
	list_filter = ('date_created',)
	list_display = ('name', 'description', 'state', 'date_modified', 'date_created')
	search_fields = ('name', 'state__name')


@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
	"""
	The transactiontype admin model.
	"""
	list_filter = ('date_created',)
	ordering = ('-date_created',)
	list_display = (
		'name', 'simple_name', 'description', 'state', 'date_modified', 'date_created')
	search_fields = (
		'name', 'state__name')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
	"""
	The transaction admin model.
	"""
	list_filter = ('date_created',)
	ordering = ('-date_created',)
	list_display = (
		'transaction_type', 'reference', 'source_ip', 'request', 'response', 'description',
		'state', 'date_modified', 'date_created')
	search_fields = (
		'transaction_type__name', 'reference', 'state__name')
