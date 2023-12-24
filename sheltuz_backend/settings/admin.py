from django.contrib import admin

from settings.models import SiteSetting


# Register your models here.
@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
	"""
	CATEGORY model admin. Defines the fields to display and which ones are searchable
	"""
	list_filter = ('page_link','seo_txt', 'seo_keyword', 'author', 'date_created', 'date_modified')
	list_display = ('page_link','seo_txt', 'seo_keyword', 'author', 'date_created', 'date_modified')
	search_fields = ('page_link','seo_txt', 'seo_keyword', 'author', 'date_created', 'date_modified')
	order_by = ('page_link','seo_txt', 'seo_keyword', 'author', 'date_created', 'date_modified')