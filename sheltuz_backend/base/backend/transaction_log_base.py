# coding=utf-8
"""
The transaction logging management.
"""
import logging

from django.db import transaction

from base.backend.service import StateService, TransactionService, TransactionTypeService
from base.backend.utils.common import get_request_data

lgr = logging.getLogger(__name__)


class TransactionLogBase(object):
	"""The class for logging transactions."""

	# noinspection PyMethodMayBeStatic
	def complete_transaction(self, transaction_obj, **kwargs):
		"""
		Marks the transaction object as complete.
		@param transaction_obj: The transaction we are updating.
		@type transaction_obj: Transaction
		@param kwargs: Any key->word arguments to pass to the method.
		@return: The transaction updated.
		@rtype: Transaction | None
		"""
		try:
			if kwargs is None:
				kwargs = {'state': StateService().get(name='Completed')}
			elif 'state' not in kwargs:
				kwargs['state'] = StateService().get(name='Completed')

			return TransactionService().update(transaction_obj.id, **kwargs)
		except Exception as e:
			lgr.exception('complete_transaction Exception: %s', e)
		return None

	# noinspection PyMethodMayBeStatic
	def log_transaction(self, transaction_type, **kwargs):
		"""
		Logs a transaction of the given type having the provided arguments.
		If transaction reference is not passed, it's generated. Same case for state, defaults to Active.
		@param transaction_type: The name of the type of transaction we are creating.
		@type transaction_type: str
		@param kwargs: Key word arguments to generate the transaction with.
		@return: The created transaction.
		@rtype: Transaction | None
		"""
		try:
			with transaction.atomic():
				# To ensure unique internal references,lock transactions
				last_ref = TransactionService(True).filter().order_by('-date_created').first()
				transaction_type = TransactionTypeService().get(name=transaction_type)
				if 'state' not in kwargs:
					kwargs['state'] = StateService().get(name="Active")

				if 'request' in kwargs:
					request = kwargs.pop('request', {})
					data = get_request_data(request)
					if data:
						kwargs['source_ip'] = kwargs.get('source_ip', None)
						kwargs['request'] = data

				return TransactionService().create(transaction_type=transaction_type, **kwargs)
		except Exception as e:
			lgr.exception('log_transaction Exception: %s', e)
		return None

	# noinspection PyMethodMayBeStatic
	def mark_transaction_failed(self, transaction_obj, **kwargs):
		"""
		Marks the transaction object as Failed.
		@param transaction_obj: The transaction we are updating.
		@type transaction_obj: Transaction
		@param kwargs: Any key->word arguments to pass to the method.
		@return: The transaction updated.
		@rtype: Transaction | None
		"""
		try:
			if kwargs is None:
				kwargs = {'state': StateService().get(name='Failed')}
			else:
				kwargs['state'] = StateService().get(name='Failed')
			return TransactionService().update(transaction_obj.id, **kwargs)
		except Exception as e:
			lgr.exception('mark_transaction_failed Exception: %s', e)
		return None
