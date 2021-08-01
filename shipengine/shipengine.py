
from shipengine import SHIP_ENGINE_API_KEY, SHIP_ENGINE_HOST
import requests
from pprint import pprint

class ShipEngine():
        
    def __init__(self):
        self.url = SHIP_ENGINE_HOST
        self.headers = {
            'Host': 'api.shipengine.com',
            'API-Key': SHIP_ENGINE_API_KEY,
            'Content-Type': 'application/json',
        }
                
        self.session = requests.Session()
        self.session.params = {}
        self.session.params['api_key'] = SHIP_ENGINE_API_KEY
        return
    
    def put(self, url, data=None, json=None, **kwargs):
        # pprint(f"url: {url}")
        # pprint(f"data: {data}")
        # pprint(f"json: {json}")
        # pprint(f"headers: {self.headers}")
        return self.session.put(url=url, data=data, json=json, headers=self.headers, **kwargs)
    
    def get(self, url, params=None, **kwargs):
        # pprint(f"url: {url}")
        # pprint(f"params: {params}")
        # pprint(f"headers: {self.headers}")
        return self.session.get(url=url, params=params, headers=self.headers, **kwargs)

    def delete(self, url, **kwargs):
        # pprint(f"url: {url}")
        # pprint(f"headers: {self.headers}")
        return self.session.delete(url=url, headers=self.headers, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        # pprint(f"url: {url}")
        # pprint(f"data: {data}")
        # pprint(f"json: {json}")
        # pprint(f"headers: {self.headers}")
        return self.session.post(url=url, data=data, json=json, headers=self.headers, **kwargs)

    def patch(self, url, data=None, json=None, **kwargs):
        # pprint(f"url: {url}")
        # pprint(f"data: {data}")
        # pprint(f"json: {json}")
        # pprint(f"headers: {self.headers}")
        return self.session.patch(url=url, data=data, json=json, headers=self.headers, **kwargs)
    