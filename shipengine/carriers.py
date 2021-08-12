from shipengine import InvalidCurrency, InvalidParameters, SE_SUCCESS, ShipEngine
from pprint import pprint

SE_CURRENCY_CODES = (
    "usd",
    "cad",
    "aud",
    "gbp",
    "eur",
    "nzd"
)


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
        '''List all carriers that have been added to this account.

        Returns True if the call was successful
        Returns False if errors were encountered.
        Response Data is stored in Carrier.response
        '''
        _endpoint = '/v1/carriers'
        response = self.get(self.url+_endpoint)
        if response.status_code == SE_SUCCESS:
            self.response = response.json()
            return True
        return False

    def get_carrier_by_id(self, carrier_id=None):
        '''Retrive carrier info by ID

        Returns True if successful.
        Returns False if errors are encountered.
        Response is stored in Carrier.response

        Required keywords:
            carrier_id          # required
                                # string (se_id) [ 1 .. 25 ] characters 
                                # ^se(-[a-z0-9]+)+$
                                # Example: se-28529731
                                # Carrier ID
        '''
        if not self.id_isvalid(carrier_id):
            raise InvalidParameters
        _endpoint = f"/v1/carriers/{carrier_id}"
        response = self.get(self.url+_endpoint)
        if response.status_code == SE_SUCCESS:
            self.response = response.json()
            return True
        return False
    
    def get_carrier_options(self, carrier_id=None):
        '''Get a list of the options available for the carrier.

        Returns True if successful.
        Returns False if errors are encountered.
        Response is stored in Carrier.response
        
        Required keywords:
            carrier_id          # required
                                # string (se_id) [ 1 .. 25 ] characters 
                                # ^se(-[a-z0-9]+)+$
                                # Example: se-28529731
                                # Carrier ID
        '''
        if not self.id_isvalid(id=carrier_id):
            raise InvalidParameters
        _endpoint = f"/v1/carriers/{carrier_id}/options"
        response = self.get(self.url+_endpoint)
        self.response = response.json()
        if response.status_code == SE_SUCCESS:
            return True
        return False

    def list_carrier_package_types(self, carrier_id=None):
        '''List the services associated with the carrier ID.

        Returns True if successful.
        Returns False if errors are encountered.
        Response is stored in Carrier.response
        
        Required keywords:
            carrier_id          # required
                                # string (se_id) [ 1 .. 25 ] characters 
                                # ^se(-[a-z0-9]+)+$
                                # Example: se-28529731
                                # Carrier ID
        '''
        if not self.id_isvalid(id=carrier_id):
            raise InvalidParameters
        _endpoint = f"/v1/carriers/{carrier_id}/packages"
        response = self.get(self.url+_endpoint)
        self.response = response.json()
        if response.status_code == SE_SUCCESS:
            return True
        return False

    def list_carrier_services(self, carrier_id=None):
        '''List the services associated with the carrier ID.

        Returns True if successful.
        Returns False if errors are encountered.
        Response is stored in Carrier.response
        
        Required keywords:
            carrier_id          # required
                                # string (se_id) [ 1 .. 25 ] characters 
                                # ^se(-[a-z0-9]+)+$
                                # Example: se-28529731
                                # Carrier ID
        '''
        if not self.id_isvalid(id=carrier_id):
            raise InvalidParameters
        _endpoint = f"/v1/carriers/{carrier_id}/services"
        response = self.get(self.url+_endpoint)
        self.response = response.json()
        if response.status_code == SE_SUCCESS:
            return True
        return False