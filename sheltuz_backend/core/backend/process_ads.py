import logging
from datetime import datetime

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from base.backend.service import StateService
from base.backend.transaction_log_base import TransactionLogBase
from base.backend.utils.common import get_client_ip, get_request_data
from context_processors.helpers import Helpers
from base.backend.service import ADService, CategoryService, LocationService, SheltuzUserService, ADBidService
from core.backend.status import SheltuzNotify

lgr = logging.getLogger(__name__)


class ProcessADs(object):
	def __init__(self, request):
		self.request_data = get_request_data(request)
		# self.request_data = kwargs
		self.request = request
		self.state_available = StateService().get(name="Available")
		self.notify = SheltuzNotify()
		self.helpers = Helpers()
		self.transaction_table = TransactionLogBase()

	def get_all_adverts(self):
		transaction = None
		source_ip = get_client_ip(self.request)
		transaction = self.transaction_table.log_transaction('GetAdverts', request=self.request, source_ip=source_ip)
		if not transaction:
			lgr.exception("Error occurred while trying to create ad bid")
			self.transaction_table.mark_transaction_failed(
				transaction, response=self.notify.failed(), message="transaction not found")
			return {"code": self.notify.info(), 'message': 'Error creating transaction'}
		try:
			products = ADService().filter(state=self.state_available)
			product_list = []
			page = self.request_data.get('page')
			if not page:
				return {"code": self.notify.failed(), "message": "page not found"}
			for product in products:
				product_data = self.helpers.convert_advert_to_json(product)
				product_list.append(product_data)
			paginator = Paginator(product_list, 8)
			try:
				page_obj = paginator.get_page(page)
			# returns the desired page object
			except PageNotAnInteger:
				# if page_number is not an integer then assign the first page
				page_obj = paginator.page(1)
			except EmptyPage:
				# if page is empty then return last page
				page_obj = paginator.page(paginator.num_pages)
			self.transaction_table.complete_transaction(transaction, response=self.notify.success(), message="Success")
			return {
				"code": self.notify.success(),
				"page_number": page_obj.number,
				"total_pages": f"Page {page_obj.number} of {paginator.num_pages}",
				"data": page_obj.object_list
			}
		except Exception as e:
			lgr.exception("Error occurred while fetching products : %s" % str(e))
			self.transaction_table.mark_transaction_failed(transaction, response=self.notify.failed(), message=str(e))
			return {"code": self.notify.failed(), "message": "Error in fetching products"}

	def get_ad_details(self):
		transaction = None
		source_ip = get_client_ip(self.request)
		transaction = self.transaction_table.log_transaction('GetAdDetails', request=self.request, source_ip=source_ip)
		if not transaction:
			lgr.exception("Error occurred while trying to create ad bid")
			self.transaction_table.mark_transaction_failed(
				transaction, response=self.notify.failed(), message="transaction not found")
			return {"code": self.notify.info(), 'message': 'Error creating transaction'}
		try:
			ad_id = self.request_data.get("id")
			if not ad_id:
				lgr.exception("Error occurred while trying to get advert: %s")
				self.transaction_table.mark_transaction_failed(
					transaction, response=self.notify.failed(), message=str(ad_id))
				return {"code": self.notify.error(), 'message': 'AD not found'}
			advert = ADService().get(id=ad_id)
			if not advert:
				return {"code": self.notify.info(), 'message': 'Ad not found'}
			data = self.helpers.convert_advert_to_json(advert)
			return {
				"code": self.notify.success(),
				"data": data
			}
		except Exception as e:
			lgr.exception("Error occurred while fetching advert : %s" % str(e))
			self.transaction_table.mark_transaction_failed(transaction, response=self.notify.failed(), message=str(e))
			return {"code": self.notify.failed(), "message": "Error in fetching advert"}

	def create_advert(self):
		transaction = None
		try:
			source_ip = get_client_ip(self.request)
			transaction = self.transaction_table.log_transaction('CreateAdvert', request=self.request, source_ip=source_ip)
			if not transaction:
				lgr.exception("Error occurred while trying to create ad bid")
				self.transaction_table.mark_transaction_failed(
					transaction, response=self.notify.failed(), message="transaction not found")
				return {"code": self.notify.info(), 'message': 'Error creating transaction'}
			user_id = self.request_data.get('user_id')
			name = self.request_data.get('name')
			description = self.request_data.get('description')
			price = self.request_data.get('price')
			location_name = self.request_data.get('location')
			category_name = self.request_data.get('category')
			condition = self.request_data.get('condition')
			model = self.request_data.get('model')
			further_location = self.request_data.get('furhter_location')
			has_waranty = self.request_data.get('has_waranty')
			gallery_image_1 = self.request_data.get('gallery_image_1', None)
			gallery_image_2 = self.request_data.get('gallery_image_2', None)
			gallery_image_3 = self.request_data.get('gallery_image_3', None)
			category = CategoryService().get(name=category_name)
			location = LocationService().get(name=location_name)
			sheltuz_user = SheltuzUserService().get(id=user_id)
			ADService().create(
				name=name, description=description, price=price, 
				location=location, category=category, author=sheltuz_user,
				condition=StateService().get(name=condition), further_location=further_location,
				has_warranty=has_waranty, gallery_image_1=gallery_image_1, model=model,
				gallery_image_2=gallery_image_2, gallery_image_3=gallery_image_3, state=StateService().get(name="Available"))
			return {
				"code": self.notify.success(),
			}
		except Exception as e:
			lgr.exception("Error occurred while trying to create advert : %s" % str(e))
			# self.transaction_table.mark_transaction_failed(transaction, response=self.notify.failed(), message=str(e))
			return {"code": self.notify.failed(), "message": "Error in create advert"}

	def create_ad_bid(self):
		transaction = None
		source_ip = get_client_ip(self.request)
		transaction = self.transaction_table.log_transaction('CreateAdBid', request=self.request, source_ip=source_ip)
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
			ad_id = self.request_data.get('ad_id')
			if not ad_id:
				lgr.exception("Error occurred while trying to get advert: %s")
				self.transaction_table.mark_transaction_failed(
					transaction, response=self.notify.failed(), message="advert not found")
				return {"code": self.notify.error_code, 'message': 'AD not found'}
			sheltuz_user = SheltuzUserService().get(id=user_id)
			advert = ADService().get(id=ad_id)
			time = datetime.now()
			ADBidService().create(
				name=str(sheltuz_user.name) + str(time),
				description="Bid Added",
				sheltuz_user=sheltuz_user,
				advert=advert)
			return {'code': self.notify.success()}
		except Exception as e:
			lgr.exception("Error occurred while trying to create ad bid: %s" % str(e))
			self.transaction_table.mark_transaction_failed(transaction, response=self.notify.failed(), message=str(e))
			return {"code": self.notify.failed(), "message": "Error in create advert"}

	def get_related_adverts(self):
		transaction = None
		try:
			source_ip = get_client_ip(self.request)
			transaction = TransactionLogBase().log_transaction('RelatedAdverts', request=self.request, source_ip=source_ip)
			if not transaction:
				return {"code": self.notify.info(), 'message': 'Error creating transaction'}
			ad_id = self.request_data.get("ad_id")
			if not ad_id:
				lgr.exception("Username not provided : %s" % ad_id)
				TransactionLogBase().mark_transaction_failed(transaction, response=self.notify.not_found())
				return {"code": self.notify.not_found(), "message": "Unable to find the username"}
			advert = ADService().get(id=ad_id)
			if advert.inventory < 0:
				return {"code": self.notify.info(), "message": "product is out of stock"}
			category = advert.category
			related_adverts = ADService().filter(category=category)
			advert_list = []
			for ad in related_adverts:
				if len(advert_list) < 4:
					advert = self.helpers.convert_advert_to_json(ad)
					advert_list.append(advert)
			TransactionLogBase().complete_transaction(transaction, response=self.notify.success(), message="Success")
			return {"code": self.notify.success(), "adverts": advert_list}
		except Exception as e:
			lgr.info("Error occurred while trying to fetch product: %s" % str(e))
			TransactionLogBase().mark_transaction_failed(transaction, response=self.notify.failed(), message=str(e))
			return {"code": self.notify.failed(), "message": "Error in fetching of products"}
