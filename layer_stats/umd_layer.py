import requests

from analysis import Analysis
from utilities import geojson_to_geostore
from utilities import google_sheet as gs

class UmdLayer(Analysis):
    '''class to define requests to UMD api. Inherits from Analysis class'''

    def __init__(self):

        super(UmdLayer, self).__init__()

    def count_loss_gain_extent(self, layer_dict, endpoint):
        '''count TC loss for each feature geostore and append the output to the dict
        :param layer_dict: dict of feature names and geostore ids
        :param endpoint: the api endpoint string
        :return: updated layer_dict with loss calculations'''

        #send analysis request record result in dict
        for key in layer_dict:
            geostore = layer_dict[key]['geostore']
            print "running analysis for {0} with geostore: {1}".format(key, geostore)

            #calculate gain and extent
            data = Analysis().analyze(endpoint, geostore)

            try:
                gain = data['data']['attributes']['gain']
                extent = data['data']['attributes']['treeExtent']
                layer_dict[key]['tc_gain'] = gain
                layer_dict[key]['tc_extent'] = extent
                print "gain and extent calculated for {}".format(key)
            except (KeyError, TypeError) as e:
                print "UMD key or type error for {0} because {1}".format(key, str(e))

            for period in self.tcloss_periods:
                data = Analysis().analyze(endpoint, geostore, self.tcloss_periods[period])

                #calculate loss by year
                try:
                    loss = data['data']['attributes']['loss']
                    layer_dict[key]['tc_loss_' + period] = loss
                    print "loss calculated for {0} at {1}".format(key, period)
                except (KeyError, TypeError) as e:
                    print "key or type error for {0} because {1}".format(key, str(e))

        #pop off geostore
        for key in layer_dict:
            layer_dict[key].pop('geostore', 0)

        return layer_dict

    def update_gs(self, layer_name):
        '''get geojson dict and calculates stats for the data
        :param layer_name: name of the datasets
        :return: updated dictionary of statsitics for umd loss, gain and extent'''

        #get layer_dict (feature name geostore id)
        layer_dict = geojson_to_geostore.create_geostore_dict(layer_name)

        #get layer stats (feature name, geostore id and loss stats)
        layer_stats = self.count_loss_gain_extent(layer_dict, 'umd-loss-gain')

        return layer_stats
