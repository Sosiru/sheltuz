from django.contrib.auth.models import User
from django.db import models

from base.models import BaseModel, State


# Create your models here.

class SheltuzUser(BaseModel):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	phone_number = models.IntegerField(null=True, blank=True)
	image = models.ImageField(upload_to='images/', blank=True, null=True)
	device = models.CharField(max_length=200, blank=True, null=True)
	state = models.ForeignKey(State, default=State.default_state, on_delete=models.CASCADE)

	REQUIRED_FIELDS = ['username']

	class Meta:
		verbose_name = "SheltuzUser"

	def __str__(self):
		return '%s %s %s %s' % (self.user.username, self.user.first_name, self.user.last_name, self.phone_number)


class PasswordResetToken(BaseModel):
	user = models.ForeignKey(SheltuzUser, on_delete=models.CASCADE)
	token = models.CharField(max_length=200, null=True, blank=True)
	state = models.ForeignKey(State, default=State.default_state, on_delete=models.CASCADE)
