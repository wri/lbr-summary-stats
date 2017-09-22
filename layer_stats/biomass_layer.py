import requests

from analysis import Analysis
from utilities import geojson_to_geostore
from utilities import google_sheet as gs

class BiomassLayer(Analysis):
    '''class to define requests to Biomass api. Inherits from Analysis class'''

    def __init__(self):

        super(BiomassLayer, self).__init__()

    def calculate_carbon_emissions(self, layer_dict, endpoint):
        '''calculate carbon emissions for each feature geostore and append the output to the dict
        :param layer_dict: dict of feature names and geostore ids
        :param endpoint: the api endpoint string
        :return: updated layer_dict with emission calculations'''

        #send analysis request record result in dict
        for key in layer_dict:
            geostore = layer_dict[key]['geostore']

            #calculate biomass stats for area
            data = Analysis().analyze(endpoint, geostore)

            try:
                carbon_emissions = data['data']['attributes']['co2LossByYear']
                for year in carbon_emissions:
                    layer_dict[key]['co2_' + year] = carbon_emissions[year]
                    print "carbon emissions calculated for {}".format(key)
            except (KeyError, TypeError) as e:
                print "Biomass key or type error for {0} because {1}".format(key, str(e))

        #pop off geostore
        for key in layer_dict:
            layer_dict[key].pop('geostore', 0)

        return layer_dict

    def update_gs(self, layer_name):

        #get layer_dict (feature name geostore id)
        layer_dict = geojson_to_geostore.create_geostore_dict(layer_name)

        #get layer stats (feature name, geostore id and loss stats)
        layer_stats = self.calculate_carbon_emissions(layer_dict, 'biomass-loss')

        return layer_stats
