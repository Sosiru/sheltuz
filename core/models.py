from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from base.models import BaseModel, GenericBaseModel, State, Country
from users.models import SheltuzUser


class PasswordToken(BaseModel):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
	token = models.CharField(max_length=100, unique=True)
	state = models.ForeignKey(State, default=State.default_state, on_delete=models.CASCADE)
	is_verified = models.BooleanField(default=False)

	def __str__(self):
		return '%s - %s' % (self.user, self.token)


class Category(GenericBaseModel):
	# parent = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
	description = models.TextField(null=True)
	is_top_category = models.BooleanField(default=False)
	image = models.ImageField(upload_to='images/', blank=True, null=True)
	state = models.ForeignKey(State, related_name="category_state", default=State.default_state, on_delete=models.CASCADE)

	class Meta:
		verbose_name_plural = 'Categories'

		indexes = [
			models.Index(fields=['name'])
		]

	def __str__(self):
		return self.name


	@classmethod
	def default_category(cls):
		"""
		The default Active state.
		@return: The active state, if it exists, or create a new one if it doesn't exist.
		@rtype: str | None
		"""
		# noinspection PyBroadException
		try:
			state = cls.objects.get(name='Fashion')
			return state.id
		except Exception:
			pass


class Location(GenericBaseModel):
	country = models.ForeignKey(Country, default=Country.default_country, on_delete=models.CASCADE)
	estate = models.CharField(max_length=30, default="Juja", blank=False)
	state = models.ForeignKey(State, related_name="location_state", default=State.default_state, on_delete=models.CASCADE)

	class Meta:
		indexes = [
			models.Index(fields=['name'])
		]

	def __str__(self):
		return self.name

	@classmethod
	def default_location(cls):
		"""
		The default Active state.
		@return: The active state, if it exists, or create a new one if it doesn't exist.
		@rtype: str | None
		"""
		# noinspection PyBroadException
		try:
			location= cls.objects.get(name='Nairobi')
			return location.id
		except Exception:
			pass


class AD(GenericBaseModel):
	price = models.IntegerField()
	category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)  # Ad belongs to a particular category
	has_warranty = models.BooleanField(default=False)
	condition = models.ForeignKey(State, null=True, blank=True, on_delete=models.SET_NULL)
	description = models.TextField()
	location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.SET_NULL)
	model = models.CharField(max_length=30, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	author = models.ForeignKey(SheltuzUser, null=True, blank=True, on_delete=models.CASCADE)
	image = models.ImageField('images', null=True, blank=True)
	gallery_image_1 = models.ImageField('images', null=True, blank=True)
	gallery_image_2 = models.ImageField('images', null=True, blank=True)
	gallery_image_3 = models.ImageField('images', null=True, blank=True)
	state = models.ForeignKey(State, related_name="ad_state", default=State.default_state,on_delete=models.CASCADE)

	class Meta:
		ordering = ('-date_created',)
		indexes = [
			models.Index(fields=['name']),
			models.Index(fields=['price']),
			models.Index(fields=['condition']),
			models.Index(fields=['category']),
			models.Index(fields=['location'])
		]

	def __str__(self):
		return self.name


class ADBid(GenericBaseModel):
	sheltuzUser = models.ForeignKey(SheltuzUser, on_delete=models.PROTECT)
	ad_product = models.ForeignKey('AD', on_delete=models.CASCADE)
	state = models.ForeignKey(State, default=State.default_state, on_delete=models.CASCADE)

	class Meta:
		ordering = ('-date_created',)
		indexes = [
			models.Index(fields=['sheltuzUser']),
			models.Index(fields=['ad_product']),
		]

	def __str__(self):
		return str(self.ad_product) + " " + self.ad_product.name



