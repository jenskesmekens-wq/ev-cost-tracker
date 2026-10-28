import requests
class PriceClient:
    def __init__(self,json_url):
        self.json_url=json_url
    def get_prices(self):
        r=requests.get(self.json_url,timeout=30)
        r.raise_for_status()
        return r.json()
