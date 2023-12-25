from django.contrib import admin
from django.contrib.auth.models import User

from core.models import AD, Location, Category, ADBid

admin.site.unregister(User)
# Register your models here.
@admin.register(AD)
class ADAdmin(admin.ModelAdmin):
	"""
	AD model admin. Defines the fields to display and which ones are searchable
	"""
	list_filter = ('name', 'price', 'category', 'location', 'state', 'condition', 'model')
	list_display = ('name', 'price', 'category', 'location', 'state', 'condition', 'model', 'has_warranty', 'date_created', 'date_modified')
	search_fields = ('name', 'price', 'category__name', 'location__name', 'condition__name', 'state__name', 'model',  'date_created', 'date_modified')
	order_by = ('name', 'price',  'model', 'date_created', 'date_modified')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
	"""
	Location model admin. Defines the fields to display and which ones are searchable
	"""
	list_filter = ('country__code','country__name', 'name', 'estate', 'state__name', 'date_created', 'date_modified')
	list_display = ('country', 'name', 'estate', 'state','date_created', 'date_modified')
	search_fields = ('country__code', 'name', 'estate','state__name', 'date_created', 'date_modified')
	order_by = ('country__code', 'name', 'estate', 'state__name', 'date_created', 'date_modified')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	"""
	CATEGORY model admin. Defines the fields to display and which ones are searchable
	"""
	list_filter = ('name', 'is_top_category', 'date_created', 'date_modified')
	list_display = ('name', 'is_top_category', 'state', 'date_created', 'date_modified')
	search_fields = ('name', 'is_top_category', 'state__name', 'date_created', 'date_modified')
	order_by = ('name',  'date_created', 'date_modified')


@admin.register(ADBid)
class ADBidAdmin(admin.ModelAdmin):
	"""
	CATEGORY model admin. Defines the fields to display and which ones are searchable
	"""
	list_filter = ('name', 'ad_product__name', 'sheltuzUser', 'ad_product__price', 'date_created', 'date_modified')
	list_display = ('name', 'ad_product', 'sheltuzUser', 'state', 'date_created', 'date_modified')
	search_fields = ('name', 'ad_product__name', 'sheltuzUser__user__username', 'ad_product__price', 'date_created', 'date_modified')
	order_by = ('name', 'ad_product', 'sheltuzUser', 'state', 'date_created', 'date_modified')




