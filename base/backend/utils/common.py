import base64
import json
import logging
import random
from datetime import datetime, date
from functools import wraps

from django.db.models import Q
from django.http import JsonResponse

lgr = logging.getLogger(__name__)


def get_request_data(request):
	"""
	Retrieves the request data irrespective of the method and type it was send.
	@param request: The Django HttpRequest.
	@type request: WSGIRequest
	@return: The data from the request as a dict
	@rtype: QueryDict
	"""
	try:
		data = None
		if request is not None:
			request_meta = getattr(request, 'META', {})
			request_method = getattr(request, 'method', None)
			if request_meta.get('CONTENT_TYPE', '') == 'application/json':
				data = json.loads(request.body)
			elif str(request_meta.get('CONTENT_TYPE', '')).startswith('multipart/form-data;'):  # Special handling for
				# Form Data?
				data = request.POST.copy()
				data = data.dict()
			elif request_method == 'GET':
				data = request.GET.copy()
				data = data.dict()
			elif request_method == 'POST':
				data = request.POST.copy()
				data = data.dict()
			if not data:
				request_body = getattr(request, 'body', None)
				if request_body:
					data = json.loads(request_body)
				else:
					data = dict()
			return data
	except Exception as e:
		return dict()


def get_reference():
	# Randomly choose a letter from all the ascii_letters
	random_letter = [chr(random.randint(ord('A'), ord('Z'))), chr(random.randint(ord('A'), ord('Z')))]
	number_gen = random.randrange(1000000, 9999999)
	return f"{random_letter[0]}{number_gen}{random_letter[1]}"


def disable_for_loaddata(signal_handler):
	"""
	Decorator that turns off signal handlers when loading fixture data.
	"""

	@wraps(signal_handler)
	def wrapper(*args, **kwargs):
		"""wrapper for the signal"""
		if kwargs.get('raw'):
			return
		signal_handler(*args, **kwargs)

	return wrapper


def normalize_date(date_text):
	"""
	Normalizes the date by converting it to a date time object
	@param date_text: The date string or instance to convert to a date object.
	@type date_text: str | datetime | date
	@return: The datetime converted accordingly.
	@rtype: datetime | None
	"""
	try:
		if isinstance(date_text, (datetime, date)):  # No need of processing
			return date_text
		valid_date_formats = [
			'%Y-%m-%d', '%Y/%m/%d', '%Y%m%d', '%d/%m/%Y', '%d-%m-%Y', '%d%m%Y', '%m/%d/%Y', '%m-%d-%Y', '%m%d%Y']
		for valid_date in valid_date_formats:
			try:
				return datetime.strptime(date_text, valid_date)
			except Exception:
				continue
	except Exception:
		pass
	return None


def generate_internal_reference(last_reference=None):
	"""
	This function generates the internal reference number.
	@param last_reference: The last reference to be generated. If None, the starting pattern is used.
	@type last_reference: str | None
	@return: The generated reference number.
	@rtype: str
	"""
	if not last_reference:
		return 'TRX-100000000'
	ref = last_reference[4:]
	r = int(ref) + 1
	return 'TRX-%s' % r


def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip


def encode_base64(string):
	string_bytes = string.encode("ascii")
	base64_bytes = base64.b64encode(string_bytes)
	return base64_bytes.decode("ascii")


def decode_base64(base64_string):
	base64_bytes = base64_string.encode("ascii")
	string_bytes = base64.b64decode(base64_bytes)
	return string_bytes.decode("ascii")


def generate_table_response(data=None, draw=1, records_filtered=0, records_total=0, error=None):
	"""
	This function generates the table response for data table consumers.
	@param data: The data from the queryset.
	@type data: list | None
	@param draw: The data-table draw param as sent form client side.
	@type draw: int
	@param records_filtered: The total records count filtered from the queryset.
	@type records_filtered: int
	@param records_total: The total records in the queryset.
	@type records_total: int
	@param error: The error string, if any.
	@type error: str | None
	@return: A JSON response with the data-table request packaged accordingly.
	@rtype: JsonResponse
	"""
	try:
		if draw is None:
			draw = []
		return JsonResponse({
			'draw': draw, 'data': data, 'error': error, 'recordsFiltered': records_filtered,
			'recordsTotal': records_total
		})
	except Exception as e:
		lgr.exception('Exception: %s', e)
	return JsonResponse({'draw': 0, 'data': [], 'error': 'Server error.', 'recordsFiltered': 0, 'recordsTotal': 0})


def get_error_table_response(draw=0, error='Error occurred retrieving data'):
	"""
	Retrieves the default DT responses in case of an error.
	@param draw: The DT draw request.
	@type draw: int
	@param error: An error message to be returned to DT.
	@type error: str
	@return: The DT dict that should be encoded accordingly.
	@rtype: dict
	"""
	return {'draw': draw, 'data': [], 'error': error, 'recordsFiltered': 0, 'recordsTotal': 0}


def pop_first_none_empty_from_list(list_items):
	"""
	Gets the fist item in the list that's not empty then removes that item from the list.
	Awesome.
	@param list_items: The items to check.
	@type list_items: list
	@return: The item that's not empty and the list with the item removed.
	@rtype: tuple
	"""
	try:
		length = len(list_items)
		local_list = list_items
		for _ in range(0, length):
			field = local_list.pop(0)  # Always pop the first item as other items might have already been removed.
			if len(str(field)) > 0:
				return field, local_list
	except Exception as e:
		lgr.exception('pop_first_none_empty_from_list Exception: %s', e)
	return '', list_items


def build_search_query(search_value, columns, extra_columns=None):
	"""
	Builds a search query using Q objects, ORed together.
	@param search_value: The value to search for.
	@param columns: Columns to carry out searching in.
	@type columns: list
	@param extra_columns: A list of Extra columns that we don't want to include on the main columns.
	@type extra_columns: list | None
	@return: Q objects
	@rtype: Q
	"""
	try:
		if isinstance(extra_columns, list):
			columns += extra_columns
		if len(str(search_value).strip()) > 0:
			if len(columns) > 0:
				field, fields = pop_first_none_empty_from_list(columns)
				query = Q(('%s__icontains' % str(field), str(search_value).strip()))
				for fl in fields:
					if fl != '' and str(search_value).strip() != '':
						query |= Q(('%s__icontains' % fl, str(search_value).strip()))
				return query
	except Exception as e:
		lgr.exception('build_search_query Exception: %s', e)
	return ~Q(date_created=None)


def extract_ordering(order, columns=list(), default_sort='-date_created'):
	"""
	Extracts the ordering from a DT request
	@param order: The DT request order field. Comes in structure [{column:0, dir: 'asc'}]
	@param columns: The columns definition according to the database models. If none is provided,
	we assume the order came with valid DB columns.
	@param default_sort: The default sorting criteria if an exception occurs. String.
	@return: A tuple with the columns sorted validly.
	@rtype: tuple
	"""
	try:
		ordering = list()
		order = list(order)
		for ord_item in order:
			ord_item = dict(ord_item)
			column = int(ord_item.get('column', 0))
			sort = str(ord_item.get('dir', 'asc'))
			# Valid sorting direction
			if sort == 'asc':
				sort = ''
			else:
				sort = '-'
			if len(columns) > column:
				if columns[column] is not None and len(str(columns[column])) > 3:
					ordering.append(str(sort + str(columns[column])))
			elif len(str(ord_item.get('column', 0))) > 3:  # Assume a named column at least 3 chars
				ordering.append(str(sort + str(ord_item.get('column', ''))))
		if len(ordering) > 0:
			return tuple(ordering)
		return default_sort,
	except Exception as e:
		lgr.exception('extract_ordering Exception: %s', e)
	return default_sort,


def extract_dt_columns(dt_columns):
	"""
	Extracts the DT columns from the request sent by DataTables.
	@param dt_columns: The list of DT columns.
	@type dt_columns: list[dict]
	@return: Returns a list of the columns by DT.
	@rtype: list
	"""
	clean_cols = list(map(lambda x: x.get('data', ''), dt_columns))
	if 'id' not in clean_cols:
		clean_cols.append('id')
	return clean_cols


def extract_not_none(columns):
	"""
	Extracts the items in the list that are not None and returns the list.
	@param columns: The list of items to
	@type columns: list
	@return: Returns the list but with the empty or None items removed.
	@rtype: list
	"""
	new_list = []
	for col in columns:
		if col is not None and len(col) > 0:
			new_list.append(col)
	return new_list
