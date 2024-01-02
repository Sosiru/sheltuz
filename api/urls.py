from django.urls import path, include

urlpatterns = [
	path('ecommerce/', include("core.urls")),
	path('billing/', include("billing.urls")),
]