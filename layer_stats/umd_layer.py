import requests

from analysis import Analysis
from utilities import geojson_to_geostore
from utilities import google_sheet as gs

class UmdLayer(Analysis):
    '''class to define requests to UMD api. Inherits from Analysis class'''

    def __init__(self):

        super(UmdLayer, self).__init__()

    def count_gain_extent(self, layer_dict, endpoint, features=None):
        '''count TC loss for each feature geostore and append the output to the dict
        :param layer_dict: dict of feature names and geostore ids
        :param endpoint: the api endpoint string
        :param features: optional list of features to update with statistics
        :return: updated layer_dict with gain, extent and total area calculations'''

        #create empty list (analysis results will be appended)
        data = {}

        #send analysis request record result in dict
        if features == None:
            for key in layer_dict:
                geostore = layer_dict[key]['geostore']
                print "running analysis for {0} with geostore: {1}".format(key, geostore)

                #get extent and gain data from analysis class
                stats = Analysis().analyze(endpoint, geostore)
                data[key] = {}
                data[key]['gain'] = stats['data']['attributes']['gain'] * 2.47105 #convert to acres
                data[key]['extent'] = stats['data']['attributes']['treeExtent'] * 2.47105 #convert to acres
                data[key]['area'] = stats['data']['attributes']['areaHa'] * 2.47105 #convert to acres

            return data

        elif features:
            for key in layer_dict:
                if key in features:
                    geostore = layer_dict[key]['geostore']
                    print "running analysis for feature {0} with geostore: {1}".format(key, geostore)

                    #get data from analysis class
                    stats = Analysis().analyze(endpoint, geostore)
                    data[key] = {}
                    data[key]['gain'] = stats['data']['attributes']['gain'] * 2.47105 #convert to acres
                    data[key]['extent'] = stats['data']['attributes']['treeExtent'] * 2.47105 #convert to acres
                    data[key]['area'] = stats['data']['attributes']['areaHa'] * 2.47105 #convert to acres
                else:
                    print "Feature not found in data during umd extent and gain analysis {}".format(features)

            return data

    def count_loss(self, layer_dict, layer_stats, endpoint, features=None):
        '''count total tree cover loss by year for each features
        :param layer_dict: geostore and feature name dictionary
        :param layer_stats: statistic dictionary of extent, gain and area stats
        :param endpoint: the api endpoint for the analyses
        :param features: optional list of specific features to update with stats
        :return: updated layer_stats dict with loss stats'''

        if features == None:
            for key in layer_stats:
                geostore = layer_dict[key]['geostore']
                try:
                    for period in self.tcloss_periods:
                        print "running loss analysis for {0} at {1}".format(key, period)
                        loss_stats = Analysis().analyze(endpoint, geostore, self.tcloss_periods[period])
                        layer_stats[key]['tc_loss_' + period] = loss_stats['data']['attributes']['loss'] * 2.47105 #convert to acres
                except (KeyError, TypeError) as e:
                    print "key or type error for {0} because {1}".format(key, str(e))

            return layer_stats

        elif features:
            for key in layer_stats:
                geostore = layer_dict[key]['geostore']

                if key in features:
                    try:
                        for period in self.tcloss_periods:
                            print "running loss analysis for {0} at {1}".format(key, period)
                            loss_stats = Analysis().analyze(endpoint, geostore, self.tcloss_periods[period])
                            layer_stats[key]['tc_loss_' + period] = loss_stats['data']['attributes']['loss'] * 2.47105 #convert to acres
                    except (KeyError, TypeError) as e:
                        print "key or type error for {0} because {1}".format(key, str(e))

                else:
                    print "feature not found in data during umd loss analysis {}".format(features)

            return layer_stats

    def update_gs(self, layer_name, features=None):
        '''get geojson dict and calculates stats for the data
        :param layer_name: name of the datasets
        :param features: optional list of specific features to update in the data
        :return: updated dictionary of statsitics for umd loss, gain and extent'''

        #get layer_dict (feature name geostore id)
        layer_dict = geojson_to_geostore.create_geostore_dict(layer_name)

        # count gain and extent
        layer_stats = self.count_gain_extent(layer_dict, 'umd-loss-gain', features)

        #get loss data
        layer_stats_all = self.count_loss(layer_dict, layer_stats, 'umd-loss-gain', features)

        return layer_stats_all
