import requests

from utilities import google_sheet as gs

class Analysis(object):

    def __init__(self):

        self.api = "http://production-api.globalforestwatch.org/"

    def analyze(self, endpoint, geostore, period=None):
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

    def combine_stats(self, tcloss_stats, tcgain_stats):
        '''combine statsitic dictionaries
        :param tcloss_stats: stats generated from TcLoss class
        :param tcgain_stats: stats generated from TcGain class'''

        # dicts = []
        # dicts.extend([tcloss_stats, tcgain_stats])
        #
        # all_stats = { k:[d[k] for d in dicts] for k in dicts[0] }
        #
        # return all_stats
        all_stats = tcloss_stats

        for key in all_stats:
            all_stats[key]['gain'] = tcgain_stats[key]['tc_gain']

        return all_stats

    def update_sheet(self, layer_name, layer_stats):
        '''method to update google sheet with layer_stats
        :param layer_name: the dataset of the Stats
        :param layer_stats: a dictionary of the statistics'''

        for id, loss_dict in layer_stats.iteritems():
            for col_name, loss_val in loss_dict.iteritems():
                try:
                    gs.set_value('Name', id, col_name, layer_name, loss_val)
                    print "loss values set for {0} at {1}".format(id, col_name)
                except ValueError, e:
                    print "value error for {0} because {1}".format(id, str(e))

        #Download spreadsheet
        csv_name = layer_name.replace(" ", "_")
        download_url = 'https://docs.google.com/spreadsheets/d/1uWL2xf7XNkRfqmfBeV-KtEKLky_4kVFA7dZIsBMjuB8/export?format=csv&id=1uWL2xf7XNkRfqmfBeV-KtEKLky_4kVFA7dZIsBMjuB8&gid=0'
        gs.download_spreadsheet(csv_name, download_url)
