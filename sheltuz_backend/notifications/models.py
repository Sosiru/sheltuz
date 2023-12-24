from django.db import models

from base.models import GenericBaseModel, State
from users.models import SheltuzUser


# Create your models here.
class NotificationBase(GenericBaseModel):
	user = models.ForeignKey(SheltuzUser, on_delete=models.CASCADE)
	state = models.ForeignKey(State, related_name="notification", on_delete=models.CASCADE, default=State.default_state)

	def __str__(self):
		return "%s" % self.name

	class Meta:
		verbose_name = 'Notification'