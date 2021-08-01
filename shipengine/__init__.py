import os
import requests

SHIP_ENGINE_API_KEY = os.environ.get('SHIP_ENGINE_API_KEY', None)
SHIP_ENGINE_HOST = 'https://api.shipengine.com'

class APIKeyMissingError(Exception):
    pass

if SHIP_ENGINE_API_KEY is None:
    raise APIKeyMissingError(
        "Usage of this wrapper requires and API"
        "vist https://www.shipengine.com/docs/ to aquire an API Key."
    )

session = requests.Session()
session.params = {}
session.params['api_key'] = SHIP_ENGINE_API_KEY


# Status Codes
SE_SUCCESS = 200	    # Success
                        # The HTTP request was successful.
SE_CREATED = 201	    # Created
                        # The requested resource was successfully created.
SE_NO_CONTENT = 204	    # NoContent
                        # The HTTP request was successful, and the response is empty.
SE_MULTI_STATUS = 207	# Multi-Status	
                        # The HTTP request was successful, but contains separate response codes that each need to be evaluated
SE_BAD_REQUEST = 400	# Bad Request
                        # There's something wrong with your request. See the error code for more details about the problem.
SE_UNAUTHORIZED = 401	# Unauthorized
                        # Your API key is invalid, expired, or has been deactivated.
SE_NOT_FOUND = 404	    # Not Found
                        # The resource you requested does not exist. For example, a request to v1/shipments/se-123456 would return a 404 status code if there is no shipment with an ID of se-123456
SE_NOT_ALLOWED = 405	# Not Allowed
                        # The HTTP method you used is not supported by ShipEngine.
SE_CONFLICT = 409	    # Conflict
                        # The request conflicts with the current state of the server. For example, you may be attempting to create a resource that already exists, or ship a package that has already been shipped.
SE_INTERNAL = 500	    # Internal Server Error
                        # The server cannot process the request. If this occurrs persistently, then please contact support for help.

from .shipengine import ShipEngine
