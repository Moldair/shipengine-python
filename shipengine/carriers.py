from shipengine import SE_SUCCESS, ShipEngine
from pprint import pprint

SE_CURRENCY_CODES = (
    "usd",
    "cad",
    "aud",
    "gbp",
    "eur",
    "nzd"
)
class InvalidCurrency(Exception):
    pass

class Carrier(ShipEngine):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._carrier = {
            "carrier_id": "",
            "carrier_code": "",
            "account_number": "",
            "requires_funded_amount": "false",
            "balance": 0.0,
            "nickname": "",
            "friendly_name": "",
            "primary": "false",
            "has_multi_package_supporting_services": "false",
            "supports_label_messages": "false",
            "services": [
            ],
            "packages": [
            ],
            "options": [
            ]
        }
        return
    def add_funds_to_carrier(self, id=None, amount=0.0, currency=None):
        if isinstance(id, str):
            _endpoint = f"/v1/carriers/{id}/add_funds"
        if isinstance(currency, str):
            if currency not in SE_CURRENCY_CODES:
                raise InvalidCurrency
        if amount >= 0.0:
            response = self.put(self.url+_endpoint, json={"currency": currency, "amount": amount})
            if response.status_code == SE_SUCCESS:
                return response.json()
        return False

    def list_carriers(self):
        _endpoint = '/v1/carriers'
        response = self.get(self.url+_endpoint)
        if response.status_code == SE_SUCCESS:
            self._carrier_list = response.json()['carriers']
            return True
        return False

    def get_carrier_by_id(self, id=None):
        _endpoint = '/v1/carriers/'
        if isinstance(id, str):
            if id != "":
                response = self.get(self.url+_endpoint+id)
                if response.status_code == SE_SUCCESS:
                    self._carrier = response.json()
                    return True
        return False
    
    def get_carrier_options(self, id=None):
        if isinstance(id, str):
            if self._carrier['carrier_id'] == id:
                return self._carrier['options']
            else:
                if self.get_carrier_by_id(id=id):
                    return self._carrier['options']
        return False

    def list_carrier_package_types(self, id=None):
        if isinstance(id, str):
            if self._carrier['carrier_id'] == id:
                return self._carrier['packages']
            else:
                if self.get_carrier_by_id(id=id):
                    return self._carrier['packages']
        return False

    def list_carrier_services(self, id=None):
        if isinstance(id, str):
            if self._carrier['carrier_id'] == id:
                return self._carrier['services']
            else:
                if self.get_carrier_by_id(id=id):
                    return self._carrier['services']
        return False