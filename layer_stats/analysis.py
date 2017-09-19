import requests

class Analysis(object):

    def __init__(self):

        self.api = "http://production-api.globalforestwatch.org/"

    def analyze(self, endpoint, period, geostore):
        '''master method to send get requests to API'''

        api_path = "http://production-api.globalforestwatch.org/" + endpoint

        payload = {'period': period, 'geostore': geostore}

        r = requests.get(api_path, params= payload)

        data = r.json()

        return data
