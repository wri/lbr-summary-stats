import requests

from analysis import Analysis
from utilities import geojson_to_geostore
from utilities import google_sheet as gs

class BiomassLayer(Analysis):
    '''class to define requests to Biomass api. Inherits from Analysis class'''

    def __init__(self):

        super(BiomassLayer, self).__init__()

    def calculate_carbon_emissions(self, layer_dict, endpoint, features=None):
        '''calculate carbon emissions for each feature geostore and append the output to the dict
        :param layer_dict: dict of feature names and geostore ids
        :param endpoint: the api endpoint string
        :return: updated layer_dict with emission calculations'''

        if features==None:
            #send analysis request record result in dict
            for key in layer_dict:
                geostore = layer_dict[key]['geostore']
                print "running analysis for {0} with geostore: {1}".format(key, geostore)

                #calculate biomass stats for area
                data = Analysis().analyze(endpoint, geostore)

                try:
                    carbon_emissions = data['data']['attributes']['co2LossByYear']
                    for year in carbon_emissions:
                        layer_dict[key]['co2_' + year] = carbon_emissions[year]
                        print "carbon emissions calculated for {}".format(key)
                except (KeyError, TypeError) as e:
                    print "Biomass key or type error for {0} because {1}".format(key, str(e))

            return layer_dict

        elif features:
            for key in layer_dict:
                if key in features:
                    geostore = layer_dict[key]['geostore']
                    print "running analysis for {0} with geostore: {1}".format(key, geostore)

                    #calculate biomass stats for area
                    data = Analysis().analyze(endpoint, geostore)

                    try:
                        carbon_emissions = data['data']['attributes']['co2LossByYear']
                        for year in carbon_emissions:
                            layer_dict[key]['co2_' + year] = carbon_emissions[year]
                            print "carbon emissions calculated for {}".format(key)
                    except (KeyError, TypeError) as e:
                        print "Biomass key or type error for {0} because {1}".format(key, str(e))

            return layer_dict

        else:

            print "features not found during biomass analysis {}".format(features)

    def update_gs(self, layer_name, features=None):
        '''get geojson dict and calculates stats for the data
        :param layer_name: name of the datasets
        :return: updated dictionary of statsitics for biomass loss'''

        #get layer_dict (feature name geostore id)
        layer_dict = geojson_to_geostore.create_geostore_dict(layer_name)
        print layer_dict

        #get layer stats (feature name, geostore id and loss stats)
        layer_stats = self.calculate_carbon_emissions(layer_dict, 'biomass-loss', features)
        print layer_stats

        return layer_stats
