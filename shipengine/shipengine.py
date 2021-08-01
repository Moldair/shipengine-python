
from shipengine import session, SHIP_ENGINE_API_KEY, SHIP_ENGINE_HOST


class ShipEngine():
        
    def __init__(self):
        self.host = SHIP_ENGINE_HOST
        self.headers = {
            'Host': 'api.shipengine.com',
            'API-Key': SHIP_ENGINE_API_KEY,
            'Content-Type': 'application/json',
        }
        return
    
    def put(self, url, data=None, json=None, **kwargs):
        return session.put(url=url, data=data, json=json, headers=self.headers, **kwargs)
    
    def get(self, url, params=None, **kwargs):
        return session.get(url=url, params=params, headers=self.headers, **kwargs)

    def delete(self, url, **kwargs):
        return session.delete(url=url, headers=self.headers, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return session.post(url=url, data=data, json=json, headers=self.headers, **kwargs)

    def patch(self, url, data=None, json=None, **kwargs):
        return session.patch(url=url, data=data, json=json, headers=self.headers, **kwargs)
    