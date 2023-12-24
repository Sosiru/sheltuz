from base.backend.transaction_log_base import TransactionLogBase
from base.backend.utils.common import get_client_ip, get_request_data
import logging
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from context_processors.helpers import Helpers
from core.backend.services import ADService
from core.backend.status import SheltuzNotify

lgr = logging.getLogger(__name__)


class SearchResultsView(object):
    def __init__(self, request):
        self.request = request
        self.request_data = get_request_data(request)
        self.transactions_table = TransactionLogBase()
        self.advert_table = ADService()
        self.helpers = Helpers()
        self.notify = SheltuzNotify()

    def get_products_queryset(self):
        transaction = None
        try:
            source_ip = get_client_ip(self.request)
            transaction = self.transactions_table.log_transaction(
                "SearchProductQueryset", request=self.request, source_ip=source_ip)
            if not transaction:
                return {"code": self.notify.info(), 'message': 'Error creating transaction'}
            search_name = self.request_data.get('search')
            page = self.request_data.get('page')
            try:
                if search_name:
                    object_list =self.advert_table.filter(name__icontains=search_name) or\
                                 self.advert_table.filter(category__name__icontains=search_name) or \
                                 self.advert_table.filter(price__icontains=search_name)
                else:
                    object_list =self.advert_table.filter()
                product_list = []
                for prod in object_list:
                    product = self.helpers.convert_advert_to_json(prod)
                    product_list.append(product)
                paginator = Paginator(product_list, 8)
                try:
                    page_obj = paginator.get_page(page)
                # returns the desired page object
                except PageNotAnInteger:
                    # if page_number is not an integer then assign the first page
                    page_obj = paginator.page(1)
                except EmptyPage:
                    # if page is empty then return last page
                    page_obj = paginator.page(paginator.num_pages)
                data = {
                    "code": self.notify.success(),
                    "page_number": page_obj.number,
                    "message": "search successful",
                    "total_pages": f"Page {page_obj.number} of {paginator.num_pages}",
                    "data": page_obj.object_list
                }
                self.transactions_table.complete_transaction(transaction, response=self.notify.success(), message="Success")
                return data
            except Exception as e:
                lgr.exception("Query not found", str(e))
                self.transactions_table.mark_transaction_failed(
                    transaction, response=self.notify.failed(), message=str(e))
                return {"code": self.notify.failed(), "message": "Error during filter"}
        except Exception as e:
            lgr.exception("Unable to search", str(e))
            self.transactions_table.mark_transaction_failed(
                transaction, response=self.notify.failed(), message=str(e))
            return {"code": self.notify.failed(), "message": "Error occurred during search"}
