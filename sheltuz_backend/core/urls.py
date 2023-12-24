from django.urls import path
from .views import GetResponse


urlpatterns = [
    path('adverts/', GetResponse.get_adverts,  name="adverts"),
    path('details/', GetResponse.get_details,  name="details"),
    path('create-ad/', GetResponse.get_create_advert,  name="create-ad"),
    path('create-ad-bid/', GetResponse.get_create_ad_bid,  name="create-ad-bid"),
    path('related-ads/', GetResponse.get_all_related_adverts,  name="related-ads"),
    path('user-ads/', GetResponse.get_adverts,  name="user-ads"),
    path('update-user-ads/', GetResponse.update_user_adverts,  name="update-user-ads"),
    path('register/', GetResponse.create_sheltuz_user,  name="register"),
    path('signin/', GetResponse.login_sheltuz_user,  name="signin"),
    path('signout/', GetResponse.logout_sheltuz_user,  name="signout"),
    path('acticate/', GetResponse.activate_sheltuz_user,  name="activate"),
    path('deactivate/', GetResponse.deactivate_sheltuz_user,  name="deactivate"),
]