from django.contrib import admin

from notifications.models import NotificationBase


# Register your models here.
@admin.register(NotificationBase)
class NotificationBaseAdmin(admin.ModelAdmin):
	"""
	CATEGORY model admin. Defines the fields to display and which ones are searchable
	"""
	list_filter = ('user', 'name', 'description', 'state__name', 'date_created', 'date_modified')
	list_display = ('user', 'name', 'description', 'state', 'date_created', 'date_modified')
	search_fields = ('user__username', 'name', 'description', 'user__first_name', 'user__last_name', 'user__email', 'state__name')
	order_by = ('user', 'name', 'description', 'date_created', 'date_modified')