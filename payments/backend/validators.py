import re
from django.conf import settings

def normalize_phone_number(phone, country_code=None, total_count=None):
    try:
        if country_code is None:
            country_code = settings.DEFAULT_COUNTRY_CODE
        if total_count is None:
            total_count = settings.PHONE_NUMBER_LENGTH
        phone = phone.replace(" ", "").replace('(', '').replace(')', '').replace('-', '')
        if str(phone).startswith('+'):
            phone = str(phone)[1:]
        if len(phone) == total_count:
            return phone
        elif (len(phone) + len(country_code)) == total_count:
            return str(country_code) + str(phone)
        elif str(phone).startswith('0') and ((len(phone) - 1) + len(country_code)) == total_count:
            return str(country_code) + str(phone)[1:]
        else:
            if len(country_code) > 0:
                overlap = abs((len(phone) + len(country_code)) - total_count)
                return str(country_code) + str(phone)[overlap - 1:]
            else:
                return phone
    except Exception as ex:
        print(ex)
    return ''


def validate_phone_number(phone_number, country_code=None, total_count=None):
    return re.match(r'^[0-9]{9,15}$', normalize_phone_number(phone_number, country_code, total_count)) is not None
