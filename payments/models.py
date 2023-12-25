from django.db import models

# Create your models here.
import uuid
from django.db import models
# from phonenumber_field.modelfields import PhoneNumberField
from base.models import State, BaseModel

STATUS = ((1, "Pending"), (0, "Complete"))


class PaymentTransaction(BaseModel):
    """This model records all the mpesa payment transactions"""
    phone_number = models.CharField(max_length=12,null=False, blank=False)
    checkout_request_id = models.CharField(max_length=200)
    reference = models.CharField(max_length=40, blank=True)
    description = models.TextField(null=True, blank=True)
    amount = models.CharField(max_length=10)
    status = models.CharField(max_length=15, choices=STATUS, default=1)
    receipt_no = models.CharField(max_length=200, blank=True, null=True)
    ip = models.CharField(max_length=200, blank=True, null=True)
    state = models.ForeignKey(State, default=State.default_state(), on_delete=models.CASCADE)

    def __unicode__(self):
        return f"{self.receipt_no}"