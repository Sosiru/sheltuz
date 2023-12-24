import logging

from django.contrib.auth.decorators import login_required
from base.backend.service import StateService
from base.backend.transaction_log_base import TransactionLogBase
from base.backend.utils.common import get_request_data, get_client_ip
from context_processors.helpers import Helpers
from base.backend.service import ADService, SheltuzUserService, LocationService, CategoryService
from core.backend.status import SheltuzNotify

lgr = logging.getLogger(__name__)


class SheltuzUserAdverts(object):
	def __init__(self, request):
		self.request_data = get_request_data(request)
		self.request = request
		self.state_available = StateService().get(name="Available")
		self.notify = SheltuzNotify()
		self.helpers = Helpers()
		self.transaction_table = TransactionLogBase()

	@login_required
	def my_ads(self):
		transaction = None
		source_ip = get_client_ip(self.request)
		transaction = self.transaction_table.log_transaction('GetAdDetails', request=self.request, source_ip=source_ip)
		if not transaction:
			lgr.exception("Error occurred while trying to create ad bid")
			self.transaction_table.mark_transaction_failed(
				transaction, response=self.notify.failed(), message="transaction not found")
			return {"code": self.notify.info(), 'message': 'Error creating transaction'}
		try:
			user_id = self.request_data.get('user_id')
			if not user_id:
				lgr.exception("Error occurred while trying to get user: %s")
				self.transaction_table.mark_transaction_failed(
					transaction, response=self.notify.failed(), message="user id not found")
				return {"code": self.notify.error_code, 'message': 'User ID not found'}
			sheltuz_user = SheltuzUserService().get(id=user_id)
			if not sheltuz_user:
				return {"code": self.notify.info(), "message": "user not found"}
			adverts = ADService().filter(author=sheltuz_user)
			advert_list = list()
			for ad in adverts:
				item = self.helpers.convert_advert_to_json(ad)
				advert_list.append(item)
			return {"code":self.notify.success(), "data":advert_list}
		except Exception as e:
			lgr.exception("Error occurred while trying to create ad bid: %s" % str(e))
			self.transaction_table.mark_transaction_failed(transaction, response=self.notify.failed(), message=str(e))
			return {"code": self.notify.failed(), "message": "Error in create advert"}

	def update_advert(self):
		transaction = None
		source_ip = get_client_ip(self.request)
		transaction = self.transaction_table.log_transaction('CreateAdBid', request=self.request, source_ip=source_ip)
		if not transaction:
			lgr.exception("Error occurred while trying to create ad bid")
			self.transaction_table.mark_transaction_failed(
				transaction, response=self.notify.failed(), message="transaction not found")
			return {"code": self.notify.info(), 'message': 'Error creating transaction'}
		try:
			ad_id = self.request_data.get('ad_id')
			name = self.request_data.get('name')
			if name:
				ADService().update(pk=ad_id, name=name)
			description = self.request_data.get('description')
			if description:
				ADService().update(pk=ad_id, description=description)
			price = self.request_data.get('price')
			if price:
				ADService().update(pk=ad_id, price=price)
			location_name = self.request_data.get('location')
			if location_name:
				location = LocationService().get(name=location_name)
				ADService().update(pk=ad_id, location=location)
			category_name = self.request_data.get('category')
			if category_name:
				category = CategoryService().get(name=category_name)
				ADService().update(pk=ad_id, category=category)
			condition = self.request_data.get('condition')
			if condition:
				ADService().update(pk=ad_id, condition=condition)
			further_location = self.request_data.get('furhter_location')
			if further_location:
				ADService().update(pk=ad_id, further_location=further_location)
			has_waranty = self.request_data.get('has_waranty')
			if has_waranty:
				ADService().update(pk=ad_id, has_waranty=has_waranty)
			gallery_image_1 = self.request_data.get('gallery_image_1')
			if gallery_image_1:
				ADService().update(pk=ad_id, gallery_image_1=gallery_image_1)
			gallery_image_2 = self.request_data.get('gallery_image_2', None)
			if gallery_image_2:
				ADService().update(pk=ad_id, gallery_image_2=gallery_image_2)
			gallery_image_3 = self.request_data.get('gallery_image_3', None)
			if gallery_image_3:
				ADService().update(pk=ad_id, gallery_image_3=gallery_image_3)
			return {
				"code": self.notify.success(),
			}
		except Exception as e:
			lgr.exception("Error occurred while trying to create advert : %s" % str(e))
			self.transaction_table.mark_transaction_failed(transaction, response=self.notify.failed(), message=str(e))
			return {"code": self.notify.failed(), "message": "Error in create advert"}


#


