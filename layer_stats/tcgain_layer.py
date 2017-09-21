import requests

from analysis import Analysis
from utilities import geojson_to_geostore
from utilities import google_sheet as gs

class TcGain(Analysis):
    '''class to define requests to UMD api. Inherits from Analysis class'''

    def __init__(self):

        super(TcGain, self).__init__()

    def count_tcgain(self, layer_dict, endpoint):
        """count TC gain for each feature geostore and append the output to the dict
        :param layer_dict: dict of feature names and geostore ids
        :param endpoint: the api endpoint string
        :return: updated layer_dict with gain calculations"""

        for key in layer_dict:
            geostore = layer_dict[key]['geostore']

            data = Analysis().analyze(endpoint, geostore)

            try:
                gain = data['data']['attributes']['gain']
                layer_dict[key]['tc_gain'] = gain
                print "gain calculated for {}".format(key)
            except KeyError, e:
                print "key error for {0} because {1}".format(key, str(e))

        #pop off geostore
        for key in layer_dict:
            layer_dict[key].pop('geostore', 0)

        return layer_dict

    def update_gs(self, layer_name):

        #get layer_dict (feature name geostore id)
        layer_dict = geojson_to_geostore.create_geostore_dict(layer_name)

        #get layer stats (feature name, geostore id and loss stats)
        layer_stats = self.count_tcgain(layer_dict, 'umd-loss-gain')

        return layer_stats
