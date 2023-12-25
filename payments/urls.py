from django.urls import path

from payments import views
urlpatterns = [
    path("checkout/", views.MpesaCheckout.as_view(), name="checkout"),
    path("callback/", views.MpesaCallBack.as_view(), name="callback"),
]