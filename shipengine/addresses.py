from shipengine import ShipEngine

class Address(ShipEngine):
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = ''
        '''
        string non-empty
        The name of a contact person at this address. This field may be set instead of - or in addition to - the company_name field.
        '''
        self._phone = ''
        '''
        string non-empty
        The phone number of a contact person at this address. The format of this phone number varies depending on the country.
        '''
        self._company_name = ''
        '''string non-empty Nullable
        If this is a business address, then the company name should be specified here.
        '''
        self._address_line1 = ''
        '''
        required
        string non-empty
        The first line of the street address. For some addresses, this may be the only line. Other addresses may require 2 or 3 lines.
        '''
        self._address_line2 = ''
        '''
        string non-empty Nullable
        The second line of the street address. For some addresses, this line may not be needed.
        '''

        self._address_line3 = ''
        '''string non-empty Nullable
        The third line of the street address. For some addresses, this line may not be needed.
        '''

        self._city_locality = ''
        '''
        required
        string non-empty
        The name of the city or locality
        '''

        self._state_province = ''
        '''
        required
        string non-empty
        The state or province. For some countries (including the U.S.) only abbreviations are allowed. Other countries allow the full name or abbreviation.
        '''

        self._postal_code = ''
        '''
        string non-empty
        postal code
        '''

        self._country_code = ''
        '''
        required
        string 2 characters
        The two-letter ISO 3166-1 country code
        '''

        self._address_residential_indicator = ''
        '''string
        Default: "unknown"
        Enum: "unknown" "yes" "no"
        Indicates whether this is a residential address.
        '''
        return

    @property
    def name(self):
        return self._name
    
    @property
    def phone(self):
        return self._phone
    
    @property
    def company_name(self):
        return self._company_name
    
    @property
    def address_line1(self):
        return self._address_line1
    
    @property
    def address_line2(self):
        return self._address_line2
    
    @property
    def address_line3(self):
        return self._address_line3
    
    @property
    def city_locality(self):
        return self._city_locality
    
    @property
    def state_province(self):
        return self._state_province
    
    @property
    def postal_code(self):
        return self._postal_code
    
    @property
    def country_code(self):
        return self._country_code
    
    @property
    def address_residential_indicator(self):
        return self._address_residential_indicator
    
    def __repr__(self):
        return f"<Address: {self.address_line1}>"
    
    def to_json(self):
        return self.__dict__
    
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
        return response

    def parse(self, text=None, knowns={}):
        '''
        Parse Text string via ShipEngine API Call
        '''
        _endpoint = '/v1/addresses/recognize'
        required_keys = [
            'text',
        ]
        if not isinstance(text, dict) or 'text' not in text.keys():
            raise Exception(
                "The text parameter should be a dictionary.\n"
                "Required keys: " + str(required_keys)
            )
        
        response = self.put(self.url+_endpoint, json=text)
        
        return response 
        
