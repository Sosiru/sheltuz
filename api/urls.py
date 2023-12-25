from django.urls import path, include

urlpatterns = [
	path('ecommerce/', include("core.urls")),
	path('payments/', include("payments.urls")),
]