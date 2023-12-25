from django.contrib import admin

from users.models import SheltuzUser, PasswordResetToken


# Register your models here.
@admin.register(SheltuzUser)
class SheltuzUserAdmin(admin.ModelAdmin):
	"""
	CATEGORY model admin. Defines the fields to display and which ones are searchable
	"""
	list_filter = (
	'user__username', 'user__first_name', 'user__last_name', 'user__email', 'phone_number', 'device', 'date_created',
	'date_modified')
	list_display = ('user', 'state', 'phone_number', 'device', 'date_created', 'date_modified')
	search_fields = (
	'user__username', 'user__first_name', 'user__last_name', 'user__email', 'state__name', 'phone_number', 'device')
	order_by = ('user', 'phone_number', 'device', 'date_created', 'date_modified')


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
	"""
	CATEGORY model admin. Defines the fields to display and which ones are searchable
	"""
	list_filter = ('user', 'token', 'state__name', 'date_created', 'date_modified')
	list_display = ('user', 'state', 'token', 'date_created', 'date_modified')
	search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email', 'state__name', 'token')
	order_by = ('user', 'token', 'date_created', 'date_modified')
