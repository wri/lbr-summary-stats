import requests

from analysis import Analysis
from utilities import geojson_to_geostore
from utilities import google_sheet as gs

class TerraiLayer(Analysis):
    '''class to define requests to TerraI api microservice. Inherits from Analysis class'''

    def __init__(self):

        super(TerraiLayer, self).__init__()

    def count_terrai_loss(self, layer_dict, endpoint):

        #send analysis request record result in dict
        for key in layer_dict:
            geostore = layer_dict[key]['geostore']

            for period in self.terrai_periods:
                data = Analysis().analyze(endpoint, geostore, self.terrai_periods[period])

                #calculate loss by year
                try:
                    loss = data['data']['attributes']['value']
                    layer_dict[key]['terrai_' + period] = loss
                    print "terrai calculated for {0} at {1}".format(key, period)
                except (KeyError, TypeError) as e:
                    print "Terra I key or type error for {0} because {1}".format(key, str(e))

        #pop off geostore
        for key in layer_dict:
            layer_dict[key].pop('geostore', 0)

        return layer_dict

    def update_gs(self, layer_name):

        #get layer_dict (feature name geostore id)
        layer_dict = geojson_to_geostore.create_geostore_dict(layer_name)

        #get layer stats (feature name, geostore id and loss stats)
        layer_stats = self.count_terrai_loss(layer_dict, 'terrai-alerts')

        return layer_stats
