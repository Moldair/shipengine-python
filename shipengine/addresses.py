from requests.models import StreamConsumedError
from shipengine import SE_SUCCESS, ShipEngine
from pprint import pprint


class Address(ShipEngine):
    STATUS_VALUES = {
        "STATUS_UNVERIFIED": "unverified",
        "STATUS_VERIFIED": "verified",
        "STATUS_WARNING": "warning",
        "STATUS_ERROR": "error",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._status = ""
        self._address = {
            'name': '',
                # string non-empty                                
                # The name of a contact person at this address. 
                # This field may be set instead of - or 
                # in addition to - the company_name field.
            'phone': '',                           
                # string non-empty
                # The phone number of a contact person at 
                # this address. The format of this phone number 
                # varies depending on the country.
            'company_name': '',                   
                # string non-empty Nullable
                # If this is a business address, then 
                # the company name should be specified here.
            'address_line1': '',                    
                # required
                # string non-empty
                # The first line of the street address. 
                # For some addresses, this may be the only 
                # line. Other addresses may require 2 or 3 lines.
            'address_line2': '',                   
                # string non-empty Nullable
                # The second line of the street address. 
                # For some addresses, this line may not be needed.
            'address_line3': '',                   
                # string non-empty Nullable
                # The third line of the street address. 
                # For some addresses, this line may not be needed.
            'city_locality': '',                    
                # required
                # string non-empty
                # The name of the city or locality
            'state_province': '',                   
                # required
                # string non-empty
                # The state or province. For some countries 
                # (including the U.S.) only abbreviations are allowed. 
                # Other countries allow the full name or abbreviation.
            'postal_code': '',                   
                # string non-empty
                # postal code
            'country_code': '',                     
                # required
                # string 2 characters
                # The two-letter ISO 3166-1 country code
            'address_residential_indicator': '',   
                # string
                # Default: "unknown"
                # Enum: "unknown" "yes" "no"
                # Indicates whether this is a residential address.
        }
        self._messages = []
        return

    @property
    def name(self):
        return self._address['name']
    
    @property
    def phone(self):
        return self._address['phone']
    
    @property
    def company_name(self):
        return self._address['company_name']
    
    @property
    def address_line1(self):
        return self._address['address_line1']
    
    @property
    def address_line2(self):
        return self._address['address_line2']
    
    @property
    def address_line3(self):
        return self._address['address_line3']
    
    @property
    def city_locality(self):
        return self._address['city_locality']
    
    @property
    def state_province(self):
        return self._address['state_province']
    
    @property
    def postal_code(self):
        return self._address['postal_code']
    
    @property
    def country_code(self):
        return self._address['country_code']
    
    @property
    def address_residential_indicator(self):
        return self._address['address_residential_indicator']
    

    def __repr__(self):
        return f"<Address: {self._address['address_line1']}>"
    
    def to_json(self):
        return self._address
    
    def validate(self, address=None):
        '''
        Validate address with ShipEngine API Call
        '''
        _endpoint = '/v1/addresses/validate'
        required_keys = [
            'address_line1',
            'city_locality',
            'state_province',
            'country_code',
        ]
        
        if not isinstance(address, list) or \
           len(address)== 0 or \
           not isinstance(address[0], dict):
            raise Exception(
                "The address parameter should be a list containing a dictionary.\n"
                "Required keys: " + str(required_keys)
            )
        
        response = self.post(self.url+_endpoint, json=address)
        data = response.json()[0]
        if response.status_code == SE_SUCCESS:
            if data['status'] == self.STATUS_VALUES['STATUS_VERIFIED']:
                self._status = data['status']
                self._address = data['matched_address']
                self._messages = data['messages']
            else:
                self._status = data['status']
                self._address = data['original_address']
                self._messages = data['messages']
            return True
        return False

    def parse(self, text=None, knowns={}):
        '''
        Parse Text string via ShipEngine API Call

        '''
        _endpoint = '/v1/addresses/recognize'
        if not isinstance(text, str):
            raise Exception("The text parameter must be a string.")
        if text == "":
            self._status = self.STATUS_VALUES['STATUS_ERROR']
            self._messages.append("Text string is too short.")
            return False
        query = {
            'text': text
        }
        query['address'] = knowns
        # pprint(f"query: {query}")
        response = self.put(self.url+_endpoint, json=query)
        data = response.json()
        # pprint(f"data: {data}")
        if response.status_code == SE_SUCCESS:
            if self.validate(address=[data['address']]):
                return True
            else:
                self._status = self.STATUS_VALUES['STATUS_WARNING']
                self._messages = ['Address validation failed.']
                
        else:
            self._status = self.STATUS_VALUES['STATUS_ERROR']
            self._messages.append(data['message'])
        
        return False
        


    def isverified(self):
        if self._status == 'verified':
            return True
        return False