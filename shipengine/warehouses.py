from vcr.patch import reset_patchers
from shipengine import InvalidParameters, SE_MULTI_STATUS, SE_NOT_FOUND, SE_NO_CONTENT, SE_SUCCESS, ShipEngine
from pprint import pprint

class Warehouse(ShipEngine):

    def __init__(self):
        super().__init__()
    
    def list_warehouses(self):
        '''Retrieve a list of warehouses associated with this account.

        Returns True on success
        Returns False if errors occured.
        Response is stored in Warehouse.response
        '''
        _endpoint = f"/v1/warehouses"
        response = self.delete(self.url+_endpoint)
        self.response = response.json()
        if response.status_code == SE_SUCCESS:
            return True
        else:
            return False

    def create_warehouse(self, warehouse_data=None):
        '''Create a warehouse location that you can use to create shipping items.
        
        Creates a  warehouse for a shipping location, then use by simply passing 
        in the generated warehouse id. If the return address is not supplied in 
        the request body then it is assumed that the origin address is 
        the return address as well.

        Returns True on success
        Returns False if errors occured.
        Response is stored in Warehouse.response

        Required keyword parameters:
            warehouse           # object
                name            # required
                                # string non-empty
                                # Name of the warehouse

                origin_address  # object
                                # The origin address of the warehouse
                
                return_address	# object
                                # The return address associated with the warehouse
        '''
        if not isinstance(warehouse_data, dict):
            raise InvalidParameters
        _endpoint='/v1/warehouses'
        response = self.post(self.url+_endpoint, json=warehouse_data)
        self.response = response.json()
        if response.status_code == SE_SUCCESS:
            return True
        else:
            return False

    def get_warehouse_by_id(self, warehouse_id=None):
        '''Retrieve warehouse data based on the warehouse ID.

        Returns True on success
        Returns False if errors occured.
        Response is stored in Warehouse.response

        Required keyword arguments:
            warehouse_id    # required
                            # string (se_id) [ 1 .. 25 ] characters 
                            # ^se(-[a-z0-9]+)+$
                            # Example: se-28529731
                            # Warehouse ID
        '''
        if not self.id_isvalid(warehouse_id):
            raise InvalidParameters
        _endpoint = f"/v1/warehouses/{warehouse_id}"
        response = self.get(self.url+_endpoint)
        self.response = response.json()
        if response.status_code == SE_SUCCESS:
            return True
        else:
            return False

    def update_warehouse_by_id(self, warehouse_id=None, warehouse_data=None):
        '''Update Warehouse object information.

        Returns True on success
        Returns False if errors occured.
        Response is stored in Warehouse.response

        Required keyword arguments:
            warehouse_id    # required
                            # string (se_id) [ 1 .. 25 ] characters 
                            # ^se(-[a-z0-9]+)+$
                            # Example: se-28529731
                            # Warehouse ID

            warehouse_data  # warehouse object
                name            # required

                origin_address  # required
                                # address object

                return_address  # optional
                                # address object
        '''
        if not self.id_isvalid(warehouse_id):
            raise InvalidParameters
        if not isinstance(warehouse_data, dict):
            raise InvalidParameters
        _endpoint = f"/v1/warehouses/{warehouse_id}"
        response = self.put(self.url+_endpoint, json=warehouse_data)
        if response.status_code == SE_NO_CONTENT:
            return True
        else:
            self.response = response.json()
            return False

    def delete_warehouse_by_id(self, warehouse_id=None):
        '''Delete a warehouse by ID.

        Returns True on success
        Returns False if errors occured.
        Response is stored in Warehouse.response

        Required keyword arguments:
            warehouse_id    # required
                            # string (se_id) [ 1 .. 25 ] characters 
                            # ^se(-[a-z0-9]+)+$
                            # Example: se-28529731
                            # Warehouse ID
        '''
        if not self.id_isvalid(warehouse_id):
            raise InvalidParameters
        _endpoint = f"/v1/warehouses/{warehouse_id}"
        response = self.delete(self.url+_endpoint)
        if response.status_code == SE_NO_CONTENT:
            return True
        else:
            self.response = response.json()
            return False