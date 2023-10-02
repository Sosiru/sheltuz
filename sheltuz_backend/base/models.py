# 200
import uuid

from django.db import models, transaction

# from base.backend.utils.common import generate_internal_reference


# Create your models here.

class BaseModel(models.Model):
	"""
	Define repetitive methods to avoid cycles of redefining in every model.
	"""
	synced = models.BooleanField(default=False)
	id = models.UUIDField(max_length=100, default=uuid.uuid4, unique=True, editable=False, primary_key=True)
	date_modified = models.DateTimeField(auto_now=True)  # (default = timezone.now)
	date_created = models.DateTimeField(auto_now_add=True)  # (default = timezone.now)

	SYNC_MODEL = False

	class Meta(object):
		abstract = True


class GenericBaseModel(BaseModel):
	"""
	Define repetitive methods to avoid cycles of redefining in every model.
	"""
	name = models.CharField(max_length=100)
	description = models.TextField(max_length=255, blank=True, null=True)

	class Meta(object):
		abstract = True


# 01
class State(GenericBaseModel):
	"States for life cycle of transactions and events"

	class Meta(object):
		ordering = ('name',)
		unique_together = ('name',)

	def __str__(self):
		return '%s ' % self.name

	@classmethod
	def default_state(cls):
		"""
		The default Active state.
		@return: The active state, if it exists, or create a new one if it doesn't exist.
		@rtype: str | None
		"""
		# noinspection PyBroadException
		try:
			state = cls.objects.get(name='Active')
			return state.id
		except Exception:
			pass

	@classmethod
	def disabled_state(cls):
		"""
		The default Disabled state.
		@return: The active state, if it exists, or create a new one if it doesn't exist.
		@rtype: str | None
		"""
		# noinspection PyBroadException
		try:
			state = cls.objects.get(name='Disabled')
			return state
		except Exception:
			pass
