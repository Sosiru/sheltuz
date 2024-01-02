# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from django.contrib import admin
from .models import PaymentTransaction, Wallet, ClientCredentials


# Register your models here.
@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
	list_display = ("phone_number", "amount",
	                "state", "transaction_id", 'date_created', 'date_modified')
	list_filter = ('phone_number', 'amount', 'date_created', 'date_modified')
	search_fields = ('name', 'phone_number', 'amount', 'date_created', 'date_modified')


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
	"""
	State model admin. Defines the fields to display and which ones are searchable
	"""
	list_filter = ('available_balance', 'actual_balance', 'date_modified', 'date_created')
	list_display = ('available_balance', 'actual_balance', 'date_modified', 'date_created')
	search_fields = ('available_balance', 'actual_balance', 'date_modified', 'date_created')


@admin.register(ClientCredentials)
class ClientCredentialsAdmin(admin.ModelAdmin):
	"""
	State model admin. Defines the fields to display and which ones are searchable
	"""
	list_filter = ('customer', 'environment', 'shortcode', 'date_modified', 'date_created')
	list_display = ('customer', 'environment', 'shortcode', 'date_modified', 'date_created')
	search_fields = ('customer', 'environment', 'shortcode', 'date_modified', 'date_created')

