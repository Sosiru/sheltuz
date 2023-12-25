from django.db import models

from base.models import BaseModel, State
from core.models import AD
from users.models import SheltuzUser


# Create your models here.


class Wishlist(BaseModel):
	customer = models.ForeignKey(SheltuzUser, related_name='wishlist_user', on_delete=models.CASCADE, blank=False, null=True)
	product = models.ForeignKey(AD, on_delete=models.CASCADE, blank=False, null=True)
	state = models.ForeignKey(State, default=State.default_state, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.customer)


class Cart(BaseModel):
	customer = models.ForeignKey(SheltuzUser, related_name='cart_user', on_delete=models.CASCADE, blank=False, null=True)
	product = models.ForeignKey(AD, on_delete=models.CASCADE, null=True)
	product_qty = models.IntegerField(null=False, blank=False, default="1")
	state = models.ForeignKey(State, default=State.default_state, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.customer)


class Order(BaseModel):
	buyer = models.ForeignKey(SheltuzUser, on_delete=models.CASCADE, null=True, blank=True)
	phone = models.IntegerField(null=True, blank=True)
	total_price = models.IntegerField(null=True, blank=True)
	paid = models.BooleanField(null=True)
	order_status = (
		('Pending', 'Pending'),
		('Packaging', 'Packaging'),
		('In transit', 'In transit'),
		('Complete', 'Complete'),
	)
	status = models.CharField(max_length=150, choices=order_status, default='Pending')
	tracking_number = models.CharField(max_length=150, null=False)
	state = models.ForeignKey(State, default=State.default_state, on_delete=models.CASCADE)

	def __str__(self):
		return '{} - {}'.format(self.id, self.tracking_number)


class OrderItem(BaseModel):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
	product = models.ForeignKey(AD, on_delete=models.CASCADE, null=True)
	product_cost = models.FloatField(null=True, blank=True)
	product_qty = models.IntegerField(null=False, blank=False, default="1")
	state = models.ForeignKey(State, default=State.default_state, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.product)
