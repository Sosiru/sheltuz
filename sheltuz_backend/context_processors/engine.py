import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from core.backend.status import SheltuzNotify
from core.backend.user_ads import SheltuzUserAdverts
from core.backend.process_ads import ProcessADs
from users.AUTHENTICATION.user_management import Authentication

lgr = logging.getLogger(__name__)
notify = SheltuzNotify()


class SheltuzProcessors(object):
    @csrf_exempt
    @staticmethod
    def all_adverts(request):
        try:
            return JsonResponse(ProcessADs(request).get_all_adverts(), safe=False)
        except Exception as e:
            lgr.exception("Could not fetch adverts", str(e))
            JsonResponse({"code": notify.error()})

    @csrf_exempt
    @staticmethod
    def get_ad_details(request):
        try:
            return JsonResponse(ProcessADs(request).get_ad_details(), safe=False)
        except Exception as e:
            lgr.exception("Could not fetch advert", str(e))
            JsonResponse({"code": notify.error()})

    @csrf_exempt
    @staticmethod
    def create_advert(request):
        try:
            return JsonResponse(ProcessADs(request).create_advert(), safe=False)
        except Exception as e:
            lgr.exception("Could not create advert", str(e))
            JsonResponse({"code": notify.error()})

    @csrf_exempt
    @staticmethod
    def create_ad_bid(request):
        try:
            return JsonResponse(ProcessADs(request).create_ad_bid(), safe=False)
        except Exception as e:
            lgr.exception("Could not create ad bid", str(e))
            JsonResponse({"code": notify.error()})


    @csrf_exempt
    @staticmethod
    def related_adverts(request):
        try:
            return JsonResponse(ProcessADs(request).get_related_adverts(), safe=False)
        except Exception as e:
            lgr.exception("Could not create ad bid", str(e))
            JsonResponse({"code": notify.error()})

    @csrf_exempt
    @staticmethod
    def user_adverts(request):
        try:
            return JsonResponse(SheltuzUserAdverts(request).my_ads(), safe=False)
        except Exception as e:
            lgr.exception("Could not create ad bid", str(e))
            JsonResponse({"code": notify.error()})

    @csrf_exempt
    @staticmethod
    def update_adverts(request):
        try:
            return JsonResponse(SheltuzUserAdverts(request).update_advert(), safe=False)
        except Exception as e:
            lgr.exception("Could not create ad bid", str(e))
            JsonResponse({"code": notify.error()})

    @csrf_exempt
    @staticmethod
    def create_sheltuz_user(request):
        try:
            return JsonResponse(Authentication(request).register_sheltuz_user(), safe=False)
        except Exception as e:
            lgr.exception("Could not create ad bid", str(e))
            JsonResponse({"code": notify.error()})


    @csrf_exempt
    @staticmethod
    def login_sheltuz_user(request):
        try:
            return JsonResponse(Authentication(request).login_sheltuz_user(), safe=False)
        except Exception as e:
            lgr.exception("Could not create ad bid", str(e))
            JsonResponse({"code": notify.error()})

    @csrf_exempt
    @staticmethod
    def logout_sheltuz_user(request):
        try:
            return JsonResponse(Authentication(request).logout_user(), safe=False)
        except Exception as e:
            lgr.exception("Could not create ad bid", str(e))
            JsonResponse({"code": notify.error()})


    @csrf_exempt
    @staticmethod
    def disable_sheltuz_user(request):
        try:
            return JsonResponse(Authentication(request).disable_sheltuz_user(), safe=False)
        except Exception as e:
            lgr.exception("Could not create ad bid", str(e))
            JsonResponse({"code": notify.error()})

    @csrf_exempt
    @staticmethod
    def enable_sheltuz_user(request):
        try:
            return JsonResponse(Authentication(request).activate_sheltuz_user(), safe=False)
        except Exception as e:
            lgr.exception("Could not create ad bid", str(e))
            JsonResponse({"code": notify.error()})

