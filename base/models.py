# 200
import uuid

from django.db import models, transaction

from base.backend.utils.common import generate_internal_reference


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


# 02
class AccountFieldType(GenericBaseModel):
	"""
	Transaction account balance type e.g. "Available", "Current", "Reserved", "Uncleared", etc
	"""
	state = models.ForeignKey(State, on_delete=models.CASCADE)

	def __str__(self):
		return '%s ' % self.name

	class Meta(object):
		ordering = ('name',)
		unique_together = ('name',)


# 03
class PaymentMethod(GenericBaseModel):
	"""
	Payment method/channel used on transactions e.g. "Paybill", "BankTransfer", "Cheque", etc
	"""
	state = models.ForeignKey(State, on_delete=models.CASCADE)

	def __str__(self):
		return '%s ' % self.name

	class Meta(object):
		ordering = ('name',)
		unique_together = ('name',)


# 04
class Country(GenericBaseModel):
	"""
	Defines countries e.g Kenya , Uganda, Tanzania
	"""
	code = models.CharField(max_length=5, null=True, unique=True)
	state = models.ForeignKey(State, on_delete=models.CASCADE)

	def __str__(self):
		return '%s' % self.code

	class Meta:
		verbose_name_plural = "Countries"

	@classmethod
	def default_country(cls):
		"""
		The default Active state.
		@return: The active state, if it exists, or create a new one if it doesn't exist.
		@rtype: str | None
		"""
		# noinspection PyBroadException
		try:
			country = cls.objects.get(code='KE')
			return country.id
		except Exception:
			pass


	@classmethod
	def disabled_country(cls):
		"""
		The default Active state.
		@return: The active state, if it exists, or create a new one if it doesn't exist.
		@rtype: str | None
		"""
		# noinspection PyBroadException
		try:
			country = cls.objects.get(code='KE')
			return country.id
		except Exception:
			pass


# 05
class TransactionType(GenericBaseModel):
	"""
	Transaction type model e.g. "WalletLoad", "WalletSpend"
	"""
	simple_name = models.CharField(max_length=50)
	is_viewable = models.BooleanField(default=False)
	state = models.ForeignKey(State, on_delete=models.CASCADE)

	def __str__(self):
		return '%s %s' % (self.name, self.simple_name)

	class Meta(GenericBaseModel.Meta):
		unique_together = ('name',)


# 06
class Transaction(BaseModel):
	"""
	The transactions happening in the system. e.g. Register,Deposit,
	"""
	transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE)
	reference = models.CharField(max_length=100, null=True, blank=True)
	source_ip = models.CharField(max_length=30, null=True, blank=True)
	request = models.TextField(null=True, blank=True)
	response = models.TextField(null=True, blank=True)
	description = models.TextField(max_length=300, null=True, blank=True)
	state = models.ForeignKey(State, on_delete=models.CASCADE)

	SYNC_MODEL = False

	def __str__(self):
		return '%s %s' % (self.transaction_type, self.reference)

	@classmethod
	def next_reference(cls, retries=0):
		"""
		Retrieves the current transaction in the DB to pass to the generator after locking the selected ID.
		This then attempts to generate a unique reference for use with the next transaction.
		@param retries: The number of times we have retried generating a unique reference.
		@type retries: int
		@return: The generated Reference.
		@rtype: str | None
		"""
		with transaction.atomic():
			last_trx = cls.objects.select_for_update().order_by('-date_created').first()
			ref = generate_internal_reference(last_trx.reference if last_trx else None)
			if cls.objects.filter(reference=ref).exists() and retries < 20:
				retries += 1
				return cls.next_reference(retries)
			return ref

	def save(self, *args, **kwargs):
		self.reference = self.next_reference()
		super(Transaction, self).save(*args, **kwargs)
