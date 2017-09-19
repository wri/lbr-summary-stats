import requests

from utilities import google_sheet as gs

class Analysis(object):

    def __init__(self):

        self.api = "http://production-api.globalforestwatch.org/"

    def analyze(self, endpoint, period, geostore):
        '''master method to send get requests to API
        :param endpoint: api endpoint
        :param period: time period of request YYYY-MM-DD,YYYY-MM-DD
        :param geostore: unique hash assigned to geojson
        :return: response from the GFW API'''

        api_path = "http://production-api.globalforestwatch.org/" + endpoint

        payload = {'period': period, 'geostore': geostore}

        try:
            r = requests.get(api_path, params= payload)
            data = r.json()
            return data
        except ValueError, e:
            print "Value Error when decoding json because {}".format(str(e))

    def update_sheet(self, layer_name, layer_stats):
        '''method to update google sheet with layer_stats
        :param layer_name: the dataset of the Stats
        :param layer_stats: a dictionary of the statistics'''

        wks = gs._open_spreadsheet(layer_name)

        total_features = len(layer_stats)

        for id, loss_dict in layer_stats.iteritems():
            for col_name, loss_val in loss_dict.iteritems():
                try:
                    gs.set_value('Name', id, col_name, layer_name, loss_val)
                    print "loss values set for {0} at {1}".format(id, col_name)
                except ValueError, e:
                    print "value error for {0} because {1}".format(id, str(e))
