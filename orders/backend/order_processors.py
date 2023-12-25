import logging
import random
import string
from base.backend.transaction_log_base import TransactionLogBase
from base.backend.utils.common import get_client_ip, get_request_data
from base.backend.service import StateService, PaymentMethodService, ADService, SheltuzUserService, CartService, OrderService, OrderItemService
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from core.backend.status import SheltuzNotify
from context_processors.helpers import Helpers

lgr = logging.getLogger(__name__)


class SheltuzOrders(object):
	def __init__(self, request):
		self.request = request
		self.request_data = get_request_data(request)
		self.notify = SheltuzNotify()
		self.mpesa_payment = PaymentMethodService().get(name="MPESA")
		self.cart_table = CartService()
		self.user_table = SheltuzUserService()
		self.transaction_table = TransactionLogBase()
		self.order_table = OrderService()
		self.product_table = ADService()
		self.order_item_table = OrderItemService()
		self.helpers = Helpers()
		self.pay_on_delivery = PaymentMethodService().get(name="Pay on Delivery")
		self.state_out_of_stock = StateService().get(name="OutOfStock")

	def place_order(self):
		transaction = None
		try:
			source_ip = get_client_ip(self.request)
			transaction = self.transaction_table.log_transaction(
				'CreateOrder', request=self.request, source_ip=source_ip)
			if not transaction:
				lgr.exception("Transaction not provided : %s")
				self.transaction_table.mark_transaction_failed(
					transaction, response=self.notify.not_found(), description="Error creating Transaction")
				return {"code": self.notify.info(), 'message': 'Error creating transaction'}
			cart_total_price = 0
			user_id = self.request_data.get("user_id")
			if not user_id:
				lgr.exception("User not provided : %s" % user_id)
				self.transaction_table.mark_transaction_failed(transaction, response=self.notify.not_found())
				return {"code": self.notify.not_found(), "message": "Unable to find username"}
			phone_number = self.request_data.get('phone_number')
			if not phone_number:
				lgr.exception("Phone number not provided : %s" % phone_number)
				self.transaction_table.mark_transaction_failed(transaction, response=self.notify.not_found())
				return {"code": self.notify.not_found(), "message": "Unable to find phone number"}
			user = self.user_table.get(id=user_id)
			"""
			Check if user account is active or not
			"""
			if not user or not user.is_active:
				lgr.exception("User not active : %s" % user_id)
				self.transaction_table.mark_transaction_failed(
					transaction, response=self.notify.not_found(),  description="User not active")
				return {"code": self.notify.not_found(), "message": "Unable to find username"}
			cart = self.cart_table.filter(customer=user)
			if not cart:
				lgr.exception("Cart object not active : %s" % user_id)
				self.transaction_table.mark_transaction_failed(
					transaction, response=self.notify.not_found(), description="Unable to find Cart object")
				return {"code": self.notify.not_found(), "message": "Unable to find Cart object"}
			item_list = []

			if len(cart) > 0:
				for item in cart:
					cart_total_price = cart_total_price + item.product.product_cost * item.product_qty
				trackno = 'marikwamare' + str(random.randint(111111, 999999))
				receipt_no = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
				order = self.order_table.get(buyer=user, tracking_number=trackno)
				if not order:
					trackno = 'MarikwaMare-' + str(random.randint(111111111, 999999999))
				new_order = self.order_table.create(
					buyer=user, phone=phone_number if phone_number else None,
					total_price=cart_total_price,
					tracking_number=trackno)
				order_status = self.helpers.convert_order_to_json(new_order)
				for item in cart:
					if item.product.inventory > 0:
						product = self.helpers.convert_cart_to_json(item)
						item_list.append(product)
						self.order_item_table.create(
							order=new_order, product=item.product, product_cost=item.product.product_cost,
							product_qty=item.product_qty)
						#  To decrease the product quantity from available stock
						order_product = ADService().filter(id=item.product.id).first()
						order_product.inventory = order_product.inventory - item.product_qty
						order_product.save()
					else:
						self.product_table.update(pk=item.id, state=self.state_out_of_stock)
						return {"code": self.notify.info(),
						        "message": "product " + item.product.name + " is out of stock"}
				# clear user's cart
				self.cart_table.filter(customer=user).delete()
				self.transaction_table.complete_transaction(
					transaction, response=self.notify.success(), message="Order Placed Successifully")
				return {"code": self.notify.success(), "message": "Order Placed Successfully",
				        "track_number": new_order.tracking_number, "order": order_status, "data": item_list}
			return {"code": self.notify.info(), "message": "Cart is Empty"}
		except Exception as e:
			lgr.exception("Order Failed failed", str(e))
			self.transaction_table.mark_transaction_failed(transaction, response=self.notify.failed(), message=str(e))
			return {"code": self.notify.failed(), "message": "Error occured while trying to place order"}

	def fetch_order(self):
		transaction = None
		try:
			source_ip = get_client_ip(self.request)
			transaction = self.transaction_table.log_transaction('FetchOrder', request=self.request,
			                                                     source_ip=source_ip)
			if not transaction:
				lgr.exception("Transaction not provided : %s")
				self.transaction_table.mark_transaction_failed(
					transaction, response=self.notify.not_found(), description="Error creating Transaction")
				return {"code": self.notify.info(), 'message': 'Error creating transaction'}
			user_id = self.request_data.get('user_id')
			if not user_id:
				lgr.exception("Username not provided : %s" % user_id)
				self.transaction_table.mark_transaction_failed(transaction, response=self.notify.not_found())
				return {"code": self.notify.not_found(), "message": "Unable to find username"}
			page = self.request_data.get("page")
			if not page:
				lgr.exception("page not provided : %s" % page)
				self.transaction_table.mark_transaction_failed(transaction, response=self.notify.not_found())
				return {"code": self.notify.not_found(), "message": "Page not found"}
			"""
			Check if user account is active or not
			"""
			user = self.user_table.get(id=user_id)
			if not user or not user.is_active:
				lgr.exception("User not active : %s" % user_id)
				self.transaction_table.mark_transaction_failed(
					transaction, response=self.notify.not_found(), description="User not active")
				return {"code": self.notify.not_found(), "message": "Unable to find username"}
			order_items = self.order_item_table.filter(order__buyer=user)
			item_list = []
			for item in order_items:
				track = item.order.tracking_number
				product = self.helpers.convert_order_item_to_json(item, track)
				print(product)
				item_list.append(product)
			paginator = Paginator(item_list, 8)
			try:
				page_obj = paginator.get_page(page)
			# returns the desired page object
			except PageNotAnInteger:
				# if page_number is not an integer then assign the first page
				page_obj = paginator.page(1)
			except EmptyPage:
				# if page is empty then return last page
				page_obj = paginator.page(paginator.num_pages)
			data = {
				"code": self.notify.success(),
				"page_number": page_obj.number,
				"total_pages": f"Page {page_obj.number} of {paginator.num_pages}",
				"data": page_obj.object_list
			}
			self.transaction_table.complete_transaction(transaction, response=self.notify.success(),
			                                            message="Order Placed Successifully")
			return {"code": self.notify.success(), "orders": data}

		except Exception as e:
			lgr.exception("Order Failed", str(e))
			self.transaction_table.mark_transaction_failed(transaction, response=self.notify.failed(), message=str(e))
			return {"code": self.notify.failed(), "message": "Error occured while trying to fetch"}

	def track_order(self):
		transaction = None
		try:
			source_ip = get_client_ip(self.request)
			transaction = self.transaction_table.log_transaction(
				'TrackOrder', request=self.request, source_ip=source_ip)
			if not transaction:
				return {"code": self.notify.info(), 'message': 'Error creating transaction'}
			user_id = self.request_data.get('user_id')
			track_number = self.request_data.get('track_number')
			if not user_id:
				lgr.exception("Username not provided : %s" % user_id)
				self.transaction_table.mark_transaction_failed(transaction, response=self.notify.not_found())
				return {"code": self.notify.not_found(), "message": "Unable to find username"}
			if not track_number:
				lgr.exception("Tracking number not provided : %s" % user_id)
				self.transaction_table.mark_transaction_failed(transaction, response=self.notify.not_found())
				return {"code": self.notify.not_found(), "message": "Unable to find tracking number"}
			"""
			Check if user account is active or not
			"""
			order = OrderService().get(tracking_number=track_number)
			if not order:
				lgr.exception("Order not found : %s" % order)
				self.transaction_table.mark_transaction_failed(transaction, response=self.notify.not_found())
				return {"code": "100.000.0003", "message": "Order Not Found"}
			data = {}
			if order:
				data = {
					"user": order.buyer.username,
					"phone_number": order.phone,
					# "receipt": order.payment_id,
					"payment_status": "Paid" if order.paid else "Not Paid",
					# "payment_mode": order.payment_mode.name,
					"total_price": order.total_price,
					"order_status": order.status
				}
			self.transaction_table.complete_transaction(
				transaction, response=self.notify.success(), message="Order Placed Successifully")
			return {"code": self.notify.success(), "order_info": data}

		except Exception as e:
			lgr.exception("Order Failed", str(e))
			self.transaction_table.mark_transaction_failed(transaction, response=self.notify.failed(),
			                                               message=str(e))
			return {"code": self.notify.failed(), "message": "Error occured while trying to fetch"}


