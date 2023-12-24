from django.urls import path, include

urlpatterns = [
	path('ecommerce/', include("core.urls")),
	path('users/', include("users.urls")),
 ]

