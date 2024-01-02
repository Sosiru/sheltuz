# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
import uuid
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from base.models import BaseModel, State
from customer.models import Customer


class PaymentTransaction(BaseModel):
    phone_number = models.CharField(max_length=30)
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    transaction_id = models.CharField(max_length=30)
    order_id = models.CharField(max_length=200)
    checkout_request_id = models.CharField(max_length=100)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.SET_NULL)
    object_id = models.PositiveIntegerField(default=0)
    content_object = GenericForeignKey('content_type', 'object_id')
    state = models.ForeignKey(State, default=State.default_state(), on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.phone_number, self.amount)


class Wallet(BaseModel):
    phone_number = models.CharField(max_length=30)
    available_balance = models.DecimalField(('available_balance'), max_digits=6, decimal_places=2, default=0)
    actual_balance = models.DecimalField(('actual_balance'), max_digits=6, decimal_places=2, default=0)
    state = models.ForeignKey(State, default=State.default_state(), on_delete=models.CASCADE)

    def __str__(self):
        return self.phone_number


class ClientCredentials(BaseModel):
    ENVIRONMENTS = [
        ('STAGE', 'STAGE'),
        ('PRODUCTION', 'PRODUCTION'),
    ]
    DEFAULT_ENVIRONMENT = "STAGE"

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    consumer_key = models.CharField(max_length=30, null=True, blank=True)
    consumer_secret = models.CharField(max_length=30, null=True, blank=True)
    shortcode = models.CharField(max_length=30, null=True, blank=True)
    pass_key = models.CharField(max_length=30, null=True, blank=True)
    auth_url = models.CharField(max_length=30, null=True, blank=True) #  e.g "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    safaricom_api = models.CharField(max_length=30, null=True, blank=True) #  e.g  "https://api.safaricom.co.ke/mpesa/stkpushquery/v1/"
    certificate_file = models.FileField(upload_to='media/', null=True, blank=True)
    host_name = models.CharField(max_length=30)
    till_number = models.CharField(max_length=30, null=True, blank=True)
    account_number = models.CharField(max_length=30, null=True, blank=True)
    trx_type = models.CharField(max_length=30) # e.g  'CustomerBuyGoodsOnline',
    environment = models.CharField(max_length=15, default=DEFAULT_ENVIRONMENT, blank=False, null=False, choices=ENVIRONMENTS)

    def __str__(self):
        return "{} {}".format(self.customer, self.environment)