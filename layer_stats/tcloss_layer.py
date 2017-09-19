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
        self.tcloss_periods['2016'] = '2016-01-01,2016-12-31'

    def count_tcloss(self, layer_dict, endpoint):
        '''count TC loss for each feature geostore and append the output to the dict
        :param layer_dict: dict of feature names and geostore ids
        :param endpoint: the api endpoint string
        :return: updated layer_dict with loss calculations'''

        for period in self.tcloss_periods:
            for key in layer_dict:
                geostore = layer_dict[key]['geostore']

                data = Analysis().analyze(endpoint, period, geostore)

                loss = data['data']['attributes']['loss']
                layer_dict[key]['tc_loss_' + period] = loss

        return layer_dict
