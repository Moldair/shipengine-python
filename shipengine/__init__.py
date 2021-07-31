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

from .shipengine import ShipEngine
