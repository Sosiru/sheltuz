import logging

from django.contrib.auth import authenticate, login, logout

from base.backend.service import SheltuzUserService, SystemUserService, StateService
from base.backend.transaction_log_base import TransactionLogBase
from base.backend.utils.common import get_request_data, get_client_ip
from context_processors.helpers import Helpers
from core.backend.status import SheltuzNotify

lgr = logging.getLogger(__name__)


# Create your views here.

class Authentication(object):
	def __init__(self, request):
		self.request_data = get_request_data(request)
		self.request = request
		self.notify = SheltuzNotify()
		self.helpers = Helpers()
		self.transaction_table = TransactionLogBase()

	def register_sheltuz_user(self):
		transaction = None
		try:
			source_ip = get_client_ip(self.request)
			transaction = self.transaction_table.log_transaction(
				'CreateSheltuzUser', request=self.request, source_ip=source_ip)
			if not transaction:
				lgr.exception("Error occurred while trying to create ad bid")
				self.transaction_table.mark_transaction_failed(
					transaction, response=self.notify.failed(), message="transaction not found")
				return {"code": self.notify.info(), 'message': 'Error creating transaction'}
			username = self.request_data.get('username')
			if not username:
				lgr.exception("Username not found")
				self.transaction_table.mark_transaction_failed(
					transaction, response=self.notify.failed(),
					message='Please provide username')
				return {'code': self.notify.error(), "message": "Please provide username"}
			first_name = self.request_data.get('first_name')
			if not first_name:
				lgr.exception("First name not found")
				self.transaction_table.mark_transaction_failed(
					transaction, response=self.notify.failed(),
					message='Please provide First name')
				return {'code': self.notify.error(), "message": "Please provide First name"}
			last_name = self.request_data.get('last_name')
			if not last_name:
				lgr.exception("Lastname not found")
				self.transaction_table.mark_transaction_failed(
					transaction, response=self.notify.failed(),
					message='Please provide Lastname')
				return {'code': self.notify.error(), "message": "Please provide Lastname"}
			email = self.request_data.get('email')
			if not email:
				lgr.exception("email not found")
				self.transaction_table.mark_transaction_failed(
					transaction, response=self.notify.failed(),
					message='Please provide email')
				return {'code': self.notify.error(), "message": "Please provide email"}
			password = self.request_data.get('password')
			if not password:
				lgr.exception("password not found")
				self.transaction_table.mark_transaction_failed(
					transaction, response=self.notify.failed(),
					message='Please provide Password')
				return {'code': self.notify.error(), "message": "Please provide Password"}
			confirm_password = self.request_data.get('confirm_password')
			if not confirm_password:
				lgr.exception("confirm password not found")
				self.transaction_table.mark_transaction_failed(
					transaction, response=self.notify.failed(),
					message='Please Confirm Password')
				return {'code': self.notify.error(), "message": "Please Confirm Password"}
			if password != confirm_password:
				lgr.exception("Password and confirm password fields did not match")
				self.transaction_table.mark_transaction_failed(
					transaction, response=self.notify.failed(),
					message='Password and confirm password fields did not match')
				return {'code': self.notify.error(), "message": "Password and confirm password fields did not match"}
			phone_number = self.request_data.get('phone_number')
			validated_phone_number = Helpers().validate_phone_number(phone_number=phone_number)
			if validated_phone_number == 'Invalid Phone number':
				self.transaction_table.mark_transaction_failed(
					transaction, response=self.notify.failed(), message='Invalid Phone number')
				return {'code': self.notify.info(), 'message': "Invalid Phone number"}
			user_information = {
				"username": username, "first_name": first_name, "last_name": last_name, "password": password, "email": email}
			system_user = self.helpers.create_user(**user_information)
			SheltuzUserService().create(user=system_user, phone_number=validated_phone_number, device=source_ip)
			self.transaction_table.complete_transaction(transaction, response=self.notify.success(), message="Success")
		except Exception as e:
			lgr.exception("Error occurred while fetching products : %s" % str(e))
			self.transaction_table.mark_transaction_failed(transaction, response=self.notify.failed(), message=str(e))
			return {'code': self.notify.error(), 'message': "Error while trying to create user"}

	def login_sheltuz_user(self):
		transaction = None
		try:
			source_ip = get_client_ip(self.request)
			transaction = self.transaction_table.log_transaction(
				'AuthenticateSheltuzUser', request=self.request, source_ip=source_ip)
			if not transaction:
				lgr.exception("Error occurred while trying to create ad bid")
				self.transaction_table.mark_transaction_failed(
					transaction, response=self.notify.failed(), message="transaction not found")
				return {"code": self.notify.info(), 'message': 'Error creating transaction'}
			username = self.request_data.get('username')
			email = self.request_data.get('email')
			if not username and not email:
				lgr.exception("Please provide username or email: %s")
				self.transaction_table.mark_transaction_failed(
					transaction, response=self.notify.failed(), message='Please provide username or email')
				return {'code': self.notify.error(), 'message': "Please provide username or email"}
			password = self.request_data.get('password')
			if not password:
				lgr.exception("Please provide password: %s")
				self.transaction_table.mark_transaction_failed(
					transaction, response=self.notify.failed(), message='Please provide password')
				return {'code': self.notify.error(), 'message': "Please provide password"}
			user = None
			if email:
				Helpers().validate_login(password=password, email=email)
				user = authenticate(email=email, password=password)
			if username:
				Helpers().validate_login(password=password, username=username)
				user = authenticate(username=username, password=password)
			login(self.request, user)
			self.transaction_table.complete_transaction(transaction, response=self.notify.success(), message="Success")
		except Exception as e:
			lgr.exception("Error occurred while fetching products : %s" % str(e))
			self.transaction_table.mark_transaction_failed(transaction, response=self.notify.failed(), message=str(e))
			return {'code': self.notify.error(), 'message': "Error while trying to create user"}

	def logout_user(self):
		transaction = None
		try:
			source_ip = get_client_ip(self.request)
			transaction = self.transaction_table.log_transaction(
				'SignoutSheltuzUser', request=self.request, source_ip=source_ip)
			if not transaction:
				lgr.exception("Error occurred while trying to create ad bid")
				self.transaction_table.mark_transaction_failed(
					transaction, response=self.notify.failed(), message="transaction not found")
				return {"code": self.notify.info(), 'message': 'Error creating transaction'}
			user_id = self.request_data.get("user_id")
			sheltuz_user = Helpers().get_sheltuz_user(user_id=user_id)
			if not sheltuz_user.user.is_active:
				lgr.exception("User is inactive")
				self.transaction_table.mark_transaction_failed(
					transaction, response=self.notify.failed(), message='User is Disabled')
				return {"code": self.notify.info(), "message": "User is disabled"}
			if not sheltuz_user.user.is_authenticated:
				lgr.exception("User is not logged in")
				self.transaction_table.mark_transaction_failed(
					transaction, response=self.notify.failed(), message='User is not logged in')
				return {"code": self.notify.info(), "message": "User is not logged in"}
			if sheltuz_user.state.name == "Active":
				logout(self.request)
				self.transaction_table.complete_transaction(
					transaction, response=self.notify.success(), message="Success")
			lgr.exception("User is inactive")
			self.transaction_table.mark_transaction_failed(
				transaction, response=self.notify.failed(), message='User is Disabled')
			return {"code": self.notify.info(), "message": "User is disabled"}
		except Exception as e:
			lgr.exception("Error occurred while fetching products : %s" % str(e))
			self.transaction_table.mark_transaction_failed(transaction, response=self.notify.failed(), message=str(e))
			return {'code': self.notify.error(), 'message': "Error while trying to create user"}

	def update_sheltuz_user_profile(self):
		transaction = None
		try:
			source_ip = get_client_ip(self.request)
			transaction = self.transaction_table.log_transaction(
				'UpdateSheltuzUser', request=self.request, source_ip=source_ip)
			if not transaction:
				lgr.exception("Error occurred while trying to create ad bid")
				self.transaction_table.mark_transaction_failed(
					transaction, response=self.notify.failed(), message="transaction not found")
				return {"code": self.notify.info(), 'message': 'Error creating transaction'}
			user_id = self.request_data.get("user_id")
			username = self.request_data.get("username")
			email = self.request_data.get("email")
			first_name = self.request_data.get("first_name")
			last_name = self.request_data.get("last_name")
			sheltuz_user = Helpers().get_sheltuz_user(user_id=user_id)
			if not sheltuz_user.user.is_active:
				lgr.exception("User is inactive")
				self.transaction_table.mark_transaction_failed(
					transaction, response=self.notify.failed(), message='User is Disabled')
				return {"code": self.notify.info(), "message": "User is disabled"}
			if sheltuz_user.state.name == "Active":
				if not username:
					username = sheltuz_user.user.username
				if not first_name:
					first_name = sheltuz_user.user.first_name
				if not last_name:
					last_name = sheltuz_user.user.last_name
				if not email:
					last_name = sheltuz_user.user.email
				SystemUserService().update(pk=sheltuz_user.user.id, username=username, email=email, last_name=last_name, first_name=first_name)
				self.transaction_table.complete_transaction(
					transaction, response=self.notify.success(), message="Success")
				return {"code": self.notify.success(), "message": "User successfully updated"}
			lgr.exception("User is inactive")
			self.transaction_table.mark_transaction_failed(
				transaction, response=self.notify.failed(), message='User is Disabled')
			return {"code": self.notify.info(), "message": "User is disabled"}
		except Exception as e:
			lgr.exception("Error occurred while fetching products : %s" % str(e))
			self.transaction_table.mark_transaction_failed(transaction, response=self.notify.failed(), message=str(e))
			return {'code': self.notify.error(), 'message': "Error while trying to create user"}

	def disable_sheltuz_user(self):
		transaction = None
		try:
			source_ip = get_client_ip(self.request)
			transaction = self.transaction_table.log_transaction(
				'DeactivateSheltuzUser', request=self.request, source_ip=source_ip)
			if not transaction:
				lgr.exception("Error occurred while trying to create ad bid")
				self.transaction_table.mark_transaction_failed(
					transaction, response=self.notify.failed(), message="transaction not found")
				return {"code": self.notify.info(), 'message': 'Error creating transaction'}
			user_id = self.request_data.get('user_id')
			if not user_id:
				lgr.exception("User id not found")
				self.transaction_table.mark_transaction_failed(
					transaction, response=self.notify.failed(), message='User not found')
				return {"code": self.notify.info(), "message": "User not found"}
			state_disabled = StateService().get("Disabled")
			user = Helpers().get_sheltuz_user(user_id=user_id)
			if user.state == state_disabled:
				return {"code": self.notify.info(), "message": "User already disabled"}
			SheltuzUserService().update(pk=user.id, state=state_disabled)
			lgr.exception("User is inactive")
			self.transaction_table.mark_transaction_failed(
				transaction, response=self.notify.failed(), message='User is Disabled')
			return {"code": self.notify.info(), "message": "User is disabled"}
		except Exception as e:
			lgr.exception("Error occurred while fetching products : %s" % str(e))
			self.transaction_table.mark_transaction_failed(transaction, response=self.notify.failed(), message=str(e))
			return {'code': self.notify.error(), 'message': "Error while trying to create user"}

	def activate_sheltuz_user(self):
		transaction = None
		try:
			source_ip = get_client_ip(self.request)
			transaction = self.transaction_table.log_transaction(
				'ActivateSheltuzUser', request=self.request, source_ip=source_ip)
			if not transaction:
				lgr.exception("Error occurred while trying to create ad bid")
				self.transaction_table.mark_transaction_failed(
					transaction, response=self.notify.failed(), message="transaction not found")
				return {"code": self.notify.info(), 'message': 'Error creating transaction'}
			user_id = self.request_data.get('user_id')
			if not user_id:
				lgr.exception("User id not found")
				self.transaction_table.mark_transaction_failed(
					transaction, response=self.notify.failed(), message='User not found')
				return {"code": self.notify.info(), "message": "User not found"}
			state_active = StateService().get("Active")
			user = Helpers().get_sheltuz_user(user_id=user_id)
			if user.state == state_active:
				return {"code": self.notify.info(), "message": "User already active"}
			SheltuzUserService().update(pk=user.id, state=state_active)
			lgr.exception("User is active")
			self.transaction_table.mark_transaction_failed(
				transaction, response=self.notify.failed(), message='User is active')
			return {"code": self.notify.info(), "message": "User is active"}
		except Exception as e:
			lgr.exception("Error occurred while fetching products : %s" % str(e))
			self.transaction_table.mark_transaction_failed(transaction, response=self.notify.failed(), message=str(e))
			return {'code': self.notify.error(), 'message': "Error while trying to create user"}

