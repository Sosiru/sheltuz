# coding=utf-8
"""
This is the service module from which all CRUD base services are declared.
"""
from django.contrib.auth.models import User

from base.backend.servicebase import ServiceBase
from base.models import State, AccountFieldType, PaymentMethod, Country, Transaction, TransactionType
from core.models import AD, ADBid, Category, Location, PasswordToken
from notifications.models import NotificationBase
from payments.models import PaymentTransaction
from settings.models import SiteSetting
from users.models import SheltuzUser
from orders.models import Order, OrderItem, Cart, Wishlist


class StateService(ServiceBase):
	"""
	State model CRUD services
	"""
	manager = State.objects


class PaymentMethodService(ServiceBase):
	"""
	PaymentMethod model CRUD services
	"""
	manager = PaymentMethod.objects


class AccountFieldTypeService(ServiceBase):
	"""
	AccountFieldType model CRUD services
	"""
	manager = AccountFieldType.objects


class CountryService(ServiceBase):
	"""
	Country model CRUD services
	"""
	manager = Country.objects


class TransactionTypeService(ServiceBase):
	"""
	TransactionType model CRUD services
	"""
	manager = TransactionType.objects


class TransactionService(ServiceBase):
	"""
	Transaction model CRUD services
	"""
	manager = Transaction.objects


class ADService(ServiceBase):
	manager = AD.objects


class ADBidService(ServiceBase):
	manager = ADBid.objects


class SheltuzUserService(ServiceBase):
	manager = SheltuzUser.objects


class SystemUserService(ServiceBase):
	manager = User.objects


class SiteSettingService(ServiceBase):
	manager = SiteSetting.objects


class CategoryService(ServiceBase):
	manager = Category.objects


class LocationService(ServiceBase):
	manager = Location.objects


class PasswordTokenService(ServiceBase):
	manager = PasswordToken.objects


class NotificationService(ServiceBase):
	manager = NotificationBase.objects


class OrderService(ServiceBase):
	manager = Order.objects


class OrderItemService(ServiceBase):
	manager = OrderItem.objects


class CartService(ServiceBase):
	manager = Cart.objects


class WishlistService(ServiceBase):
	manager = Wishlist.objects

class PaymentTransactionService(ServiceBase):
	manager = PaymentTransaction.objects
