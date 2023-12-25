from context_processors.engine import SheltuzProcessors


class GetResponse(object):
	@staticmethod
	def get_adverts(request):
		return SheltuzProcessors().all_adverts(request)

	@staticmethod
	def get_details(request):
		return SheltuzProcessors().get_ad_details(request)

	@staticmethod
	def get_create_advert(request):
		return SheltuzProcessors().create_advert(request)

	@staticmethod
	def get_create_ad_bid(request):
		return SheltuzProcessors().create_ad_bid(request)

	@staticmethod
	def get_all_related_adverts(request):
		return SheltuzProcessors().related_adverts(request)

	@staticmethod
	def get_user_related_adverts(request):
		return SheltuzProcessors().user_adverts(request)

	@staticmethod
	def update_user_adverts(request):
		return SheltuzProcessors().update_adverts(request)

	@staticmethod
	def create_sheltuz_user(request):
		return SheltuzProcessors().create_sheltuz_user(request)

	@staticmethod
	def login_sheltuz_user(request):
		return SheltuzProcessors().login_sheltuz_user(request)

	@staticmethod
	def logout_sheltuz_user(request):
		return SheltuzProcessors().logout_sheltuz_user(request)

	@staticmethod
	def activate_sheltuz_user(request):
		return SheltuzProcessors().enable_sheltuz_user(request)

	@staticmethod
	def deactivate_sheltuz_user(request):
		return SheltuzProcessors().disable_sheltuz_user(request)
