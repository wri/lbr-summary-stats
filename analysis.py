import requests

class Analysis

    def make_analysis(self, endpoint, period, geostore_id):
        '''master method to send get requests to API'''

        api_path = "http://production-api.globalforestwatch.org/" + endpoint

        parameters = {'period'= period,
                      'geostore' = geostore}

        r = requests.get(api_path, params= parameters)

        data = r.json()

        return data
