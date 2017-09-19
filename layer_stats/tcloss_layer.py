import requests

from analysis import Analysis
from utilities import geojson_to_geostore

class TcLoss(Analysis):
    '''class to define requests to UMD api. Inherits from Analysis class'''

    def __init__(self):

        super(TcLoss, self).__init__()

        #create period dict
        self.tcloss_periods = {}
        self.tcloss_periods['2000'] = '2000-01-01,2000-12-31'
        self.tcloss_periods['2001'] = '2001-01-01,2001-12-31'
        self.tcloss_periods['2002'] = '2002-01-01,2002-12-31'
        self.tcloss_periods['2003'] = '2003-01-01,2003-12-31'
        self.tcloss_periods['2004'] = '2004-01-01,2004-12-31'
        self.tcloss_periods['2005'] = '2005-01-01,2005-12-31'
        self.tcloss_periods['2006'] = '2006-01-01,2006-12-31'
        self.tcloss_periods['2007'] = '2007-01-01,2007-12-31'
        self.tcloss_periods['2008'] = '2008-01-01,2008-12-31'
        self.tcloss_periods['2009'] = '2009-01-01,2009-12-31'
        self.tcloss_periods['2010'] = '2010-01-01,2010-12-31'
        self.tcloss_periods['2011'] = '2011-01-01,2011-12-31'
        self.tcloss_periods['2012'] = '2012-01-01,2012-12-31'
        self.tcloss_periods['2013'] = '2013-01-01,2013-12-31'
        self.tcloss_periods['2014'] = '2014-01-01,2014-12-31'
        self.tcloss_periods['2015'] = '2015-01-01,2015-12-31'

    def count_tcloss(self, layer_dict, endpoint):
        '''count TC loss for each feature geostore and append the output to the dict
        :param layer_dict: dict of feature names and geostore ids
        :param endpoint: the api endpoint string
        :return: updated layer_dict with loss calculations'''

        #send analysis request record result in dict
        for key in layer_dict:
            geostore = layer_dict[key]['geostore']

            for period in self.tcloss_periods:
                data = Analysis().analyze(endpoint, self.tcloss_periods[period], geostore)

                try:
                    loss = data['data']['attributes']['loss']
                    layer_dict[key]['tc_loss_' + period] = loss
                    print "loss calculated for {0} at {1}".format(key, period)
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
        layer_stats = self.count_tcloss(layer_dict, 'umd-loss-gain')

        #update google spreadsheet with layer stats
        Analysis().update_sheet(layer_name, layer_stats)
