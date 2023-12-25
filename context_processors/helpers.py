import base64
import re

from django.contrib.auth.hashers import make_password

from base.backend.service import SheltuzUserService, SystemUserService, CountryService
regex = re.compile('[A_Za-z]')


class Helpers(object):
    @staticmethod
    def get_response_image(image_path):
        try:
            with open(str(image_path), "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return encoded_string
        except Exception as ex:
            print(ex)
            return {"999.999.999"}

    @staticmethod
    def convert_advert_to_json(item):
        try:
            return {
                "product_id": item.id,
                "name": item.name,
                "category": item.category.name,
                "image": Helpers().get_response_image(item.image),
                "cost": item.product_cost,
                "product_status": item.product_status,
                "inventory": item.inventory,
                "description": item.description,
                "discount":item.percentage_discount,
                "old_price": int(item.product_cost) - int(item.discounts),
                "product_state": item.state.name
            }
        except Exception as ex:
            print(ex)
            return {"999.999.999"}

    @staticmethod
    def convert_cart_to_json(item):
        try:
            return {
                "product_id": item.product.id,
                "name": item.product.name,
                "product_qty": item.product_qty,
                "category": item.product.category.name,
                "image": Helpers().get_response_image(item.product.image),
                "cost": item.product.product_cost,
                "discount": item.product.percentage_discount,
                "product_status": item.product.product_status,
                "inventory": item.product.inventory,
                "product_state": item.state.name
            }
        except Exception as ex:
            print(ex)
            return  {"999.999.999"}

    @staticmethod
    def get_system_user(user_id):
        try:
            user = SystemUserService().get(user_id=user_id)
            if not user:
                raise Exception('User not found')
            return user
        except Exception as ex:
            print(ex)
            return  {"999.999.999"}

    @staticmethod
    def get_sheltuz_user(user_id):
        try:
            user = SheltuzUserService().get(user__id=user_id)
            if not user:
                raise Exception('User not found')
            return user
        except Exception as ex:
            print(ex)
            return  {"999.999.999"}

    @staticmethod
    def convert_order_item_to_json(item, track):
        try:
            return {
                "product_id": item.product.id,
                "name": item.product.name,
                "product_qty": item.product_qty,
                "category": item.product.category.name,
                "image": Helpers().get_response_image(item.product.image),
                "cost": item.product.product_cost,
                'track': track,
                "discount": item.product.percentage_discount,
                "product_status": item.product.product_status,
                "inventory": item.product.inventory,
                "product_state": item.state.name
            }
        except Exception as ex:
            print(ex)
            return  {"999.999.999"}

    @staticmethod
    def convert_wishlist_to_json(item):
        try:
            return {
                "product_id": item.product.id,
                "name": item.product.name,
                "category": item.product.category.name,
                "image": Helpers().get_response_image(item.product.image),
                "cost": item.product.product_cost,
                "product_status": item.product.product_status,
                "inventory": item.product.inventory,
                "product_state": item.state.name
            }
        except Exception as ex:
            print(ex)
            return  {"999.999.999"}

    @staticmethod
    def convert_order_to_json(new_order):
        try:
            return {
                "payment": "Paid" if new_order.paid else "Not Paid",
                # "payment_mode": new_order.payment_mode.name,
                "total_price": new_order.total_price,
                "order_status": new_order.status,
                # "receipt": new_order.payment_id
            }
        except Exception as ex:
            print(ex)
            return {"999.999.999"}

    @staticmethod
    def create_hashed_password(password):
        try:
            return make_password(password)
        except Exception as ex:
            print(ex)
            return {"999.999.999"}

    @staticmethod
    def create_user(**kwargs):
        try:
            username = kwargs.get('username')
            if SystemUserService().get(username=username):
                raise Exception('user already exists')
            first_name = kwargs.get('first_name')
            last_name = kwargs.get('last_name')
            email = kwargs.get('email')
            if SystemUserService().get(email=email):
                raise Exception('user already exists')
            password = kwargs.get('password')
            hashed_password = Helpers().create_hashed_password(password)
            return SystemUserService().create(
                username=username, first_name=first_name, last_name=last_name, email=email, password=hashed_password
            )
        except Exception as ex:
            print(ex)
            return {"999.999.999"}

    @staticmethod
    def validate_phone_number(phone_number):
        try:
            if len(phone_number) > 10 and phone_number.startswith('07'):
                message= 'Invalid Phone number'
            elif phone_number.startswith('254') and len(phone_number) > 12:
                message = 'Invalid Phone number'
            elif regex.search(phone_number):
                message = 'Invalid Phone number'
            else:
                message = phone_number
            return message
        except Exception as ex:
            print(ex)
            return {"999.999.999"}


    @staticmethod
    def validate_login(password, username=None, email=None):
        try:
            user = None
            if not username and not email:
                raise Exception('Username or email missing')
            if username and not email:
                user = SystemUserService().get(username=username)
            elif email and not username:
                user = SystemUserService().get(email=email)
            if not user.is_active:
                raise Exception('user is not active')
            return user.check_password(password)
        except Exception as ex:
            print(ex)
            return {"999.999.999"}
