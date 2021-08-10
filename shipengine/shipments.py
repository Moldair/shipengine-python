from shipengine import InvalidParameters, SE_MULTI_STATUS, SE_NOT_FOUND, SE_NO_CONTENT, SE_SUCCESS, ShipEngine


class Shipment(ShipEngine):

    def __init__(self):
        super().__init__()
    
    
    def list_shipments(self, params=None):
        '''Querys shipengine.com and retrieves shipments. Returned data is stored in Shipment.response variable.

        Optional keyword arguments:
        params -- Dictionary containing optional query parameters.
            shipment_status     # Enum: "pending" "processing" "label_purchased" "cancelled"
                                # The possible shipment status values
            batch_id            # string (se_id) [ 1 .. 25 ] characters ^se(-[a-z0-9]+)+$ 
                                # Example: batch_id=se-28529731
                                # Batch ID
            tag                 # string non-empty, Example: tag=Letters_to_santa
                                # Search for shipments based on the custom tag added to the shipment object
            created_at_start    # string <date-time>, Example: created_at_start=2019-03-12T19:24:13.657Z
                                # Used to create a filter for when a resource was created 
                                # (ex. A shipment that was created after a certain time)
            created_at_end      # string <date-time>
                                # Example: created_at_end=2019-03-12T19:24:13.657Z
                                # Used to create a filter for when a resource was created, 
                                # (ex. A shipment that was created before a certain time)
            modified_at_start   # string <date-time> 
                                # Example: modified_at_start=2019-03-12T19:24:13.657Z
                                # Used to create a filter for when a resource was modified 
                                # (ex. A shipment that was modified after a certain time)
            modified_at_end     # string <date-time> 
                                # Example: modified_at_end=2019-03-12T19:24:13.657Z
                                # Used to create a filter for when a resource was modified 
                                # (ex. A shipment that was modified before a certain time)
            page                # integer >= 1, Default:1
                                # Return a specific page of results. Defaults to the first page. If set to a 
                                # number that's greater than the number of pages of results, an 
                                # empty page is returned.
            page_size           # integer >= 1, Default:25
                                # The number of results to return per response.
            sales_order_id      # string
                                # Sales Order ID
            sort_dir            # Enum: "asc" "desc", Default: "desc"
                                # Controls the sort order of the query.
            sort_by             # Enum: "modified_at" "created_at"
                                # The possible shipments sort by values

        '''
        _endpoint = "/v1/shipments"
        
        if isinstance(params, dict):
            for k in params:
                if isinstance(params[k], str):
                    if params[k] == "":
                        raise InvalidParameters
                if isinstance(params[k], int):
                    if params[k] < 1:
                        raise InvalidParameters
            response = self.get(self.url+_endpoint, params=params)
            if response.status_code == SE_SUCCESS:
                self.shipments = response.json()
        else:
            raise InvalidParameters
        return False
    
    def get_shipment_by_external_id(self, params=None):
        '''Querys shipengine.com and retrieves an individual shipment that was created using your own custom ID convention.

        Returns True if a valid shipment was found. The shipment information is 
        stored in Shipment.shipment variable.

        Returns False if an Error occurs.  Check Shipment.response to investigate error.

        Required keyword arguments:
        params -- Dictionary containing query parameters.
            Required keys:
                external_shipment_id    # string
                                        # Example: 0bcb569d-1727-4ff9-ab49-b2fec0cee5ae
                                        # ID of the shipment you are querying
                                        # Warning: The external_shipment_id is limited to 50 characters. 
                                        # Any additional characters will be truncated.
        '''
        # TODO: remove external_shipment_id from params dictionary and add it as a keyword
        if isinstance(params, dict):
            _endpoint = False
            if 'external_shipment_id' in params.keys():
                if params['external_shipment_id'] != '':
                    _endpoint = f"/v1/shipments/{params['external_shipment_id'][:50]}"
                else:
                    raise InvalidParameters
            else:
                raise InvalidParameters
            response = self.get(self.url+_endpoint)
            if response.status_code == SE_SUCCESS:
                self.shipment = response.json()
                return True
            else:
                self.response = response.json()
                return False
                
        else:
            raise InvalidParameters
    
    def get_shipment_by_id(self, params=None):
        '''Querys shipengine.com and retrieves an individual shipment based on its ID.

        Returns True if a valid shipment was found. The shipment information is 
        stored in Shipment.shipment variable.

        Returns False if an Error occurs.  Check Shipment.response to investigate error.

        Required keyword arguments:
        params -- Dictionary containing query parameters.
            Required keys:
                shipment_id     # string (se_id) [ 1 .. 25 ] characters ^se(-[a-z0-9]+)+$
                                # Example: se-28529731
                                # Shipment ID
        '''
        # TODO: remove shipment_id from params dictionary and add it as a keyword
        if isinstance(params, dict):
            _endpoint = False
            if 'shipment_id' in params.keys():
                if params['shipment_id'] != '':
                    _endpoint = f"/v1/shipments/{params['shipment_id']}"
                else:
                    raise InvalidParameters
            else:
                raise InvalidParameters
            response = self.get(self.url+_endpoint)
            if response.status_code == SE_SUCCESS:
                self.shipment = response.json()
                return True
            else:
                self.response = response.json()
                return False
                
        else:
            raise InvalidParameters

    def get_shipment_errors(self, params=None):
        '''Querys shipengine.com and retrieves errors associated with the shipment.
        
        If there are no errors associated with this shipment then the API will return 
        a 404 Not Found response to indicate that no errors are associated with the request 
        this is returned as a False Value.

        If errors are present True is returned and errors and response is stored in Shipment.response.


        Required keyword arguments:
        params -- Dictionary containing query parameters.
            Required keys:
                shipment_id     # ID of the shipment you are querying
            
            Optional keys:
                page            # integer <int32> >= 1
                                # Default: 1
                                # Example: page=2
                                # Return a specific page of results. Defaults to the first page. 
                                # If set to a number that's greater than the number of pages of 
                                # results, an empty page is returned.
                pagesize        # integer <int32> >= 1

        '''
        # TODO: remove shipment_id from params dictionary and add it as a keyword
        if isinstance(params, dict):
            _endpoint = False
            if 'shipment_id' in params.keys():
                if params['shipment_id'] != '':
                    _endpoint = f"/v1/shipments/{params['shipment_id']}/errors"
                else:
                    raise InvalidParameters
            else:
                raise InvalidParameters
            valid_keys = ['page','pagesize']
            params = dict([(key, val) for key, val in params.items() if key in valid_keys and val >= 1])
            response = self.get(self.url+_endpoint, params=params)
            if response.status_code == SE_NOT_FOUND:
                return True
            else:
                self.response = response.json()
                return False
                
        else:
            raise InvalidParameters

    def get_shipment_rates(self, params=None):
        '''Querys shipengine.com and retrieves rate information associated with the shipment ID. 
        
        Returns True on success, rate information stored in Shipment.response variable.
        Returns False if errors occur, error information stored in Shipment.response variable.

        Required keyword arguments:
        params -- Dictionary containing query parameters.
            Required keys:
                shipment_id     # ID of the shipment you are querying
            
            Optional keys:
                created_at -- Datetime filter to exclude shipements created before a certain time.

        '''
        # TODO: remove shipment_id from params dictionary and add it as a keyword
        if isinstance(params, dict):
            _endpoint = False
            if 'shipment_id' in params.keys():
                if params['shipment_id'] != '':
                    _endpoint = f"/v1/shipments/{params['shipment_id']}/rates"
                else:
                    raise InvalidParameters
            else:
                raise InvalidParameters
            valid_keys = ['created_at']
            params = dict([(key, val) for key, val in params.items() if key in valid_keys and val])
            response = self.get(self.url+_endpoint, params=params)
            self.response = response.json()
            if response.status_code == SE_SUCCESS:
                return True
            else:
                return False
                
        else:
            raise InvalidParameters

    def parse_shipping_info(self, text=None, shipment=None):
        '''Parses unstructured text and extracts shipping data.

        The shipment-recognition API makes it easy for you to extract shipping data from 
        unstructured text, including people's names, addresses, package weights and 
        dimensions, insurance and delivery requirements, and more.

        Data often enters your system as unstructured text (for example: emails, 
        SMS messages, support tickets, or other documents). ShipEngine's 
        shipment-recognition API helps you extract meaningful, structured data 
        from this unstructured text. The parsed shipment data is returned in the 
        same structure that's used for other ShipEngine APIs, so you can easily 
        use the parsed data to create a shipping label.

        Note: Shipment recognition is currently supported for the United States, 
        Canada, Australia, New Zealand, the United Kingdom, and Ireland.

        Returns:
            True upon successful query. 
            False if errors occured. 
            
            Stores returned information from ShipEngine in Shipment.response variable.

        Required keyword arguments:
            text                    # string non-empty
                                # The unstructured text that contains shipping-related entities

        Optional keyword arguments:
            shipment                #object
                                    # You can optionally provide a shipment object containing any 
                                    # already-known values. For example, you probably already know 
                                    # the ship_from address, and you may also already know what 
                                    # carrier and service you want to use.

            
                carrier_id	        # string [ 1 .. 25 ] characters ^se(-[a-z0-9]+)+$
                                    # The carrier account that is billed for the shipping charges

                service_code        # string ^[a-z0-9]+(_[a-z0-9-]+)* ?$
                                    # The carrier service used to ship the package, such as 
                                    # fedex_ground, usps_first_class_mail, flat_rate_envelope, etc.

                external_order_id   # string Nullable
                                    # ID that the Order Source assigned

                items               # Array of objects
                                    # Default: []
                                    # Describe the packages included in this shipment as 
                                    # related to potential metadata that was imported from 
                                    # external order sources

                tax_identifiers	    # Array of objects Nullable
                                    # external_shipment_id	
                                    # string <= 50 characters Nullable
                                    # You can optionally use this field to store your 
                                    # own identifier for this shipment.

                                    # Warning: The external_shipment_id is limited to 50 characters. 
                                    # Any additional characters will be truncated.

                ship_date	        # string <date-time> 
                                    # ^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[-+]\d{2}:\d{2}))?$
                                    # The date that the shipment was (or will be) shippped.
                                    # ShipEngine will take the day of week into consideration.
                                    # For example, if the carrier does not operate on Sundays, then a
                                    # package that would have shipped on Sunday will ship on Monday instead.
                ship_to	            # object 
                                    # The recipient's mailing address

                ship_from           # object
                                    # The shipment's origin address. 
                                    # If you frequently ship from the same location, consider 
                                    # creating a warehouse. Then you can simply specify the 
                                    # warehouse_id rather than the complete address each time.

                warehouse_id        # string [ 1 .. 25 ] characters Nullable ^se(-[a-z0-9]+)+$
                                    # Default: null
                                    # The warehouse that the shipment is being shipped from. 
                                    # Either warehouse_id or ship_from must be specified.

                return_to           # object
                                    # The return address for this shipment. Defaults to the ship_from address.

                confirmation        # string
                                    # Default: "none"
                                    # Enum: "none" "delivery" "signature" "adult_signature" 
                                    #       "direct_signature" "delivery_mailed"
                                    # The type of delivery confirmation that is required for this shipment.

                customs             # object Nullable
                                    # Default: null
                                    # Customs information. This is usually only needed for international shipments.

                advanced_options    # object
                                    # Advanced shipment options. These are entirely optional.

                origin_type         # string Nullable
                                    # Enum: "pickup" "drop_off"
                                    # Indicates if the package will be picked up or dropped off by the carrier

                insurance_provider  # string
                                    # Default: "none"
                                    # Enum: "none" "shipsurance" "carrier" "third_party"
                                    # The insurance provider to use for any insured packages in the shipment.

                order_source_code   # string
                                    # Enum: "amazon_ca" "amazon_us" "brightpearl" 
                                    #       "channel_advisor" "cratejoy" "ebay" "etsy" 
                                    #       "jane" "groupon_goods" "magento" "paypal" 
                                    #       "seller_active" "shopify" "stitch_labs" "squarespace" 
                                    #       "three_dcart" "tophatter" "walmart" 
                                    #       "woo_commerce" "volusion"
                                    # The order sources that are supported by ShipEngine

                packages            # Array of objects non-empty
                                    # The packages in the shipment.
                                    # Note: Some carriers only allow one package per shipment. 
                                    # If you attempt to create a multi-package shipment for a 
                                    # carrier that doesn't allow it, an error will be returned.
        '''
        if not isinstance(text, str) or text == "":
            raise InvalidParameters
        else:
            data = {'text': text}
        if shipment:
            if not isinstance(shipment, dict):
                raise InvalidParameters
            else:
                data['shipment'] = shipment
        _endpoint = '/v1/shipments/recognize'

        response = self.put(self.url+_endpoint,json=data)
        self.response = response.json()
        if response == SE_SUCCESS:
            return True
        else:
            return False

    def update_shipment_by_id(self, shipment_id=None, data=None):
        '''Queries ShipEngine.com and updates shipment info.

        Returns True if the request was successful.  Response data is stored in Shipment.response.
        Returns False if an error is encoutered. Error data is stored in Shipment.response.

        Required path parameters:
            shipment_id         # string (se_id) [ 1 .. 25 ] characters ^se(-[a-z0-9]+)+$
                                # Example: se-28529731
                                # Shipment ID

        Request data schema: application/json
            Required Keys: ['ship_to','ship_from'] See ShipEngine API for more details.

            carrier_id	            # string [ 1 .. 25 ] characters ^se(-[a-z0-9]+)+$
                                    # The carrier account that is billed for the shipping charges

            service_code	        # string ^[a-z0-9]+(_[a-z0-9-]+)* ?$
                                    # The carrier service used to ship the package, such as fedex_ground, 
                                    # usps_first_class_mail, flat_rate_envelope, etc.

            external_order_id	    # string Nullable
                                    # ID that the Order Source assigned

            items                   # Array of objects
                                    # Default: []
                                    # Describe the packages included in this shipment as related to 
                                    # potential metadata that was imported from external order sources

            tax_identifiers	        # Array of objects Nullable

            external_shipment_id	# string <= 50 characters Nullable
                                    # You can optionally use this field to store your own 
                                    # identifier for this shipment.

                                    # Warning: The external_shipment_id is limited to 50 characters. 
                                    # Any additional characters will be truncated.

            ship_date               # string <date-time> 
                                    # ^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[-+]\d{2}:\d{2}))?$
                                    # The date that the shipment was (or will be) shippped. ShipEngine 
                                    # will take the day of week into consideration. For example, 
                                    # if the carrier does not operate on Sundays, then a package that 
                                    # would have shipped on Sunday will ship on Monday instead.

            ship_to                 # required
                                    # object
                                    # The recipient's mailing address

            ship_from               # required
                                    # object
                                    # The shipment's origin address. If you frequently ship from the 
                                    # same location, consider creating a warehouse. Then you can 
                                    # simply specify the warehouse_id rather than the complete 
                                    # address each time.

            warehouse_id	        # string [ 1 .. 25 ] characters Nullable ^se(-[a-z0-9]+)+$
                                    # Default: null
                                    # The warehouse that the shipment is being shipped from. Either 
                                    # warehouse_id or ship_from must be specified.

            return_to               # object
                                    # The return address for this shipment. 
                                    # Defaults to the ship_from address.

            confirmation            # string
                                    # Default: "none"
                                    # Enum: "none" "delivery" "signature" "adult_signature" 
                                    #       "direct_signature" "delivery_mailed"
                                    # The type of delivery confirmation that is required 
                                    # for this shipment.

            customs                 # object Nullable
                                    # Default: null
                                    # Customs information. This is usually only needed for 
                                    # international shipments.

            advanced_options        # object
                                    # Advanced shipment options. These are entirely optional.

            origin_type             # string Nullable
                                    # Enum: "pickup" "drop_off"
                                    # Indicates if the package will be picked up or dropped 
                                    # off by the carrier

            insurance_provider      # string
                                    # Default: "none"
                                    # Enum: "none" "shipsurance" "carrier" "third_party"
                                    # The insurance provider to use for any insured packages 
                                    # in the shipment.

            order_source_code       # string
                                    # Enum: "amazon_ca" "amazon_us" "brightpearl" 
                                    #       "channel_advisor" "cratejoy" "ebay" "etsy" "jane" 
                                    #       "groupon_goods" "magento" "paypal" "seller_active"
                                    #       "shopify" "stitch_labs" "squarespace" "three_dcart"
                                    #        "tophatter" "walmart" "woo_commerce" "volusion"
                                    # The order sources that are supported by ShipEngine

            packages                # Array of objects non-empty
                                    # The packages in the shipment.
                                    # Note: Some carriers only allow one package per shipment. 
                                    # If you attempt to create a multi-package shipment for a 
                                    # carrier that doesn't allow it, an error will be returned.

            validate_address        # string
                                    # Default: "no_validation"
                                    # Enum: "no_validation" "validate_only" "validate_and_clean"
                                    # The possible validate address values
        '''
        if not self.id_isvalid(id=shipment_id):
            raise InvalidParameters
        _endpoint = "/v1/shipments/{shipment_id}"
        if not isinstance(data, dict):
            raise InvalidParameters
        response = self.put(self.url+_endpoint,json=data)
        self.response = response.json()
        if response == SE_SUCCESS:
            return True
        else:
            return False

    def cancel_shipment_by_id(self, shipment_id=None):
        '''Queries ShipEngine.com to mark a shipment as canceled.

        Mark a shipment cancelled, if it is no longer needed or being used by your 
        organized. Any label associated with the shipment needs to be voided first.
        An example use case would be if a batch label creation job is going to run 
        at a set time and only queries pending shipments. Marking a shipment as 
        cancelled would remove it from this process.

        Returns True on sucessful request.
        Returns False if errors are encountered. Error stored in Shipment.response.

        Required path parameters:
            shipment_id         # string (se_id) [ 1 .. 25 ] characters ^se(-[a-z0-9]+)+$
                                # Example: se-28529731
                                # Shipment ID
        
        '''
        if not self.id_isvalid(id=shipment_id):
            raise InvalidParameters
        _endpoint = f"/v1/shipments/{shipment_id}/cancel"
        response = self.put(self.url+_endpoint)
        if response.status_code == SE_NO_CONTENT:
            return True
        else:
            self.response = response.json()
            return False

    def create_shipment(self, shipments=None):
        '''Create one or multiple shipments.

        Returns True is object creation is successful.
        Returns False if errors are encountered.
        Response data stored in Shipment.response.

        Required keywords:
            shipments           # Array of objects non-empty
                                # A list of shipment objects to be created.


                Array -- Required items = ['carrier_id', 'service_code', 'ship_to', 'ship_from']
                validate_address	# string
                                    # Default: "no_validation"
                                    # Enum: "no_validation" 
                                    #       "validate_only" 
                                    #       "validate_and_clean"
                                    # The possible validate address values

                carrier_id          # required
                                    # string [ 1 .. 25 ] characters 
                                    # ^se(-[a-z0-9]+)+$
                                    # The carrier account that is billed for 
                                    # the shipping charges

                service_code        # required
                                    # string ^[a-z0-9]+(_[a-z0-9-]+)* ?$
                                    # The carrier service used to ship the package, 
                                    # such as fedex_ground, usps_first_class_mail, 
                                    # flat_rate_envelope, etc.

                external_order_id	# string Nullable
                                    # ID that the Order Source assigned

                items	            # Array of objects
                                    # Default: []
                                    # Describe the packages included in this shipment 
                                    # as related to potential metadata that was 
                                    # imported from external order sources

                tax_identifiers	    # Array of objects Nullable

                external_shipment_id	
                                    # string <= 50 characters Nullable
                                    # You can optionally use this field to store your 
                                    # own identifier for this shipment.
                                    # Warning: The external_shipment_id is limited to 50 characters. 
                                    # Any additional characters will be truncated.

                ship_date	        # string <date-time> 
                                    # ^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[-+]\d{2}:\d{2}))?$
                                    # The date that the shipment was (or will be) shippped. 
                                    # ShipEngine will take the day of week into consideration. 
                                    # For example, if the carrier does not operate on Sundays, then 
                                    # a package that would have shipped on Sunday will ship on 
                                    # Monday instead.

                ship_to             # required
                                    # object
                                    # The recipient's mailing address

                ship_from           # required
                                    # object
                                    # The shipment's origin address. If you frequently ship from the 
                                    # same location, consider creating a warehouse. Then you can simply
                                    # specify the warehouse_id rather than the complete address each time.

                warehouse_id	    # string [ 1 .. 25 ] characters Nullable ^se(-[a-z0-9]+)+$
                                    # Default: null
                                    # The warehouse that the shipment is being shipped from. 
                                    # Either warehouse_id or ship_from must be specified.

                return_to           # object
                                    # The return address for this shipment. Defaults to the 
                                    # ship_from address.

                confirmation        # string
                                    # Default: "none"
                                    # Enum: "none" "delivery" "signature" "adult_signature" 
                                    #       "direct_signature" "delivery_mailed"
                                    # The type of delivery confirmation that is required for this shipment.

                customs             # object Nullable
                                    # Default: null
                                    # Customs information. This is usually only needed 
                                    # for international shipments.

                advanced_options    # object
                                    # Advanced shipment options. These are entirely optional.

                origin_type         # string Nullable
                                    # Enum: "pickup" "drop_off"
                                    # Indicates if the package will be picked up or dropped 
                                    # off by the carrier

                insurance_provider  # string
                                    # Default: "none"
                                    # Enum: "none" "shipsurance" "carrier" "third_party"
                                    # The insurance provider to use for any insured packages in the shipment.

                order_source_code   # string
                                    # Enum: "amazon_ca" "amazon_us" "brightpearl" "channel_advisor" 
                                    #       "cratejoy" "ebay" "etsy" "jane" "groupon_goods" "magento" 
                                    #       "paypal" "seller_active" "shopify" "stitch_labs" "squarespace" 
                                    #       "three_dcart" "tophatter" "walmart" "woo_commerce" "volusion"
                                    # The order sources that are supported by ShipEngine

                packages            # Array of objects non-empty
                                    # The packages in the shipment.
                                    # Note: Some carriers only allow one package per shipment. If you 
                                    # attempt to create a multi-package shipment for a carrier that doesn't 
                                    # allow it, an error will be returned.
        '''
        # POST
        if isinstance(shipments, dict):
            shipments = [shipments]
        if not isinstance(shipments, list):
            raise InvalidParameters
        _endpoint = f"/v1/shipments"
        response = self.post(self.url+_endpoint, json=shipments)
        self.response = response.json()
        if response.status_code == SE_SUCCESS:
            return True
        else:
            return False

    def add_tag(self, shipment_id=None, tag_name=None):
        '''Adds tag to an existing shipment object.

        Returns True if object creation was successful.
        Returns False if errors were encountered. Errors are stored in Shipment.response

        Required path parameters:
            shipment_id         # string (se_id) [ 1 .. 25 ] characters ^se(-[a-z0-9]+)+$
                                # Example: se-28529731
                                # Shipment ID
            
            tag_name            # string (tag_name) non-empty
                                # Example: Fragile
                                # Tags are arbitrary strings that you can use to categorize 
                                # shipments. For example, you may want to use tags to 
                                # distinguish between domestic and international shipments, 
                                # or between insured and uninsured shipments. Or maybe you 
                                # want to create a tag for each of your customers so you 
                                # can easily retrieve every shipment for a customer.
        '''
        if not self.id_isvalid(id=shipment_id):
            raise InvalidParameters
        if not isinstance(tag_name, str):
            raise InvalidParameters
        if tag_name == "":
            raise InvalidParameters
        _endpoint = f"/v1/shipments/{shipment_id}/tags/{tag_name}"
        response = self.post(self.url+_endpoint)
        if response.status_code == SE_SUCCESS:
            return True
        else:
            self.response = response.json()
            return False
        
    def remove_tag(self, shipment_id=None, tag_name=None):
        '''Remove an existing tag from the Shipment object
        
        Returns True if the request was successful.
        Returns False if errors were encountered. Errors are stored in Shipment.response

        Required path parameters:
            shipment_id         # string (se_id) [ 1 .. 25 ] characters ^se(-[a-z0-9]+)+$
                                # Example: se-28529731
                                # Shipment ID
            
            tag_name            # string (tag_name) non-empty
                                # Example: Fragile
                                # Tags are arbitrary strings that you can use to categorize 
                                # shipments. For example, you may want to use tags to 
                                # distinguish between domestic and international shipments, 
                                # or between insured and uninsured shipments. Or maybe you 
                                # want to create a tag for each of your customers so you 
                                # can easily retrieve every shipment for a customer.
        '''
        if not self.id_isvalid(id=shipment_id):
            raise InvalidParameters
        if not isinstance(tag_name, str):
            raise InvalidParameters
        if tag_name == "":
            raise InvalidParameters
        _endpoint = f"/v1/shipments/{shipment_id}/tags/{tag_name}"
        response = self.delete(self.url+_endpoint)
        if response.status_code == SE_NO_CONTENT:
            return True
        else:
            self.response = response.json()
            return False
    