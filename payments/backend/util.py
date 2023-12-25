import logging
import time
import math
import base64
from datetime import datetime
import requests
from requests.auth import HTTPBasicAuth
from rest_framework.response import Response
from phonenumber_field.phonenumber import PhoneNumber

from base.backend.service import PaymentTransactionService
from sheltuz import  settings
from .serializers import TransactionSerializer

logging = logging.getLogger("default")
now = datetime.now()


class MpesaGateWay:
    shortcode = None
    consumer_key = None
    consumer_secret = None
    access_token_url = None
    access_token = None
    access_token_expiration = None
    checkout_url = None
    timestamp = None

    def __init__(self):
        self.consumer_key = settings.consumer_key
        print(self.consumer_key)
        self.consumer_secret = settings.consumer_secret
        self.access_token_url = settings.access_token_url
        self.shortcode = settings.shortcode
        self.password = self.generate_password()
        self.c2b_callback = settings.mpesa_query_check_url
        self.checkout_url = settings.querycheckout_url
        self.transaction_service = PaymentTransactionService()
        self.headers = None
        try:
            self.access_token = self.get_access_token()
            if self.access_token is None:
                raise Exception("Request for access token failed.")
        except Exception as e:
            logging.error("Error {}".format(e))
        else:
            self.access_token_expiration = time.time() + 3400

    def get_access_token(self):
        try:
            res = requests.get(
                self.access_token_url,
                auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret),
            )
            print(res.json())
            token = res.json()["access_token"]
            print(token)
            self.headers = {"Authorization": "Bearer %s" % token}
            return token
        except Exception as err:
            logging.error("Error {}".format(err))
            raise err

    class Decorators:
        @staticmethod
        def refresh_token(decorated):
            def wrapper(gateway, *args, **kwargs):
                if (
                    gateway.access_token_expiration
                    and time.time() > gateway.access_token_expiration
                ):
                    token = gateway.getAccessToken()
                    gateway.access_token = token
                return decorated(gateway, *args, **kwargs)

            return wrapper

    def generate_password(self):
        """Generates mpesa api password using the provided shortcode and passkey"""
        self.timestamp = now.strftime("%Y%m%d%H%M%S")
        password_str = self.shortcode + settings.pass_key + self.timestamp
        password_bytes = password_str.encode("ascii")
        return base64.b64encode(password_bytes).decode("utf-8")

    @Decorators.refresh_token
    def stk_push_request(self, payload):
        request = payload["request"]
        data = payload["data"]
        amount = data["amount"]
        phone_number = data["phone_number"]
        req_data = {
            "BusinessShortCode": self.shortcode,
            "Password": self.password,
            "Timestamp": self.timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": math.ceil(float(amount)),
            "PartyA": phone_number,
            "PartyB": self.shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": self.c2b_callback,
            "AccountReference": "Test",
            "TransactionDesc": "Test",
        }

        res = requests.post(
            self.checkout_url, json=req_data, headers=self.headers, timeout=30
        )
        res_data = res.json()
        logging.info("Mpesa request data {}".format(req_data))
        logging.info("Mpesa response info {}".format(res_data))

        if res.ok:
            data["ip"] = request.META.get("REMOTE_ADDR")
            data["checkout_request_id"] = res_data["CheckoutRequestID"]
            self.transaction_service.create(**data)
        return res_data

    def check_status(self, data):
        try:
            status = data["Body"]["stkCallback"]["ResultCode"]
        except Exception as e:
            logging.error(f"Error: {e}")
            status = 1
        return status

    def get_transaction_object(self, data):
        checkout_request_id = data["Body"]["stkCallback"]["CheckoutRequestID"]
        transaction = self.transaction_service.get(checkout_request_id=checkout_request_id)
        return transaction

    def handle_successful_pay(self, data, transaction):
        amount = None
        phone_number = None
        receipt_no = None
        items = data["Body"]["stkCallback"]["CallbackMetadata"]["Item"]
        for item in items:
            if item["Name"] == "Amount":
                amount = item["Value"]
            elif item["Name"] == "MpesaReceiptNumber":
                receipt_no = item["Value"]
            elif item["Name"] == "PhoneNumber":
                phone_number = item["Value"]

        transaction.amount = amount
        transaction.phone_number = PhoneNumber(raw_input=phone_number)
        transaction.receipt_no = receipt_no
        transaction.confirmed = True
        return transaction

    def callback_handler(self, data):
        status = self.check_status(data)
        transaction = self.get_transaction_object(data)
        if status == 0:
            self.handle_successful_pay(data, transaction)
        else:
            transaction.status = 1

        transaction.status = status
        transaction.save()

        transaction_data = TransactionSerializer(transaction).data

        logging.info("Transaction completed info {}".format(transaction_data))

        return Response({"status": "ok", "code": 0}, status=200)