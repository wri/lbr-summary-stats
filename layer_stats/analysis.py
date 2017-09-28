import requests
import requests_cache

from utilities import google_sheet as gs

class Analysis(object):

    def __init__(self):

        self.api = "http://production-api.globalforestwatch.org/"

        #create period dict for Terra I
        self.terrai_periods = {}
        self.terrai_periods['2004'] = '2004-01-01,2004-12-31'
        self.terrai_periods['2005'] = '2005-01-01,2005-12-31'
        self.terrai_periods['2006'] = '2006-01-01,2006-12-31'
        self.terrai_periods['2007'] = '2007-01-01,2007-12-31'
        self.terrai_periods['2008'] = '2008-01-01,2008-12-31'
        self.terrai_periods['2009'] = '2009-01-01,2009-12-31'
        self.terrai_periods['2010'] = '2010-01-01,2010-12-31'
        self.terrai_periods['2011'] = '2011-01-01,2011-12-31'
        self.terrai_periods['2012'] = '2012-01-01,2012-12-31'
        self.terrai_periods['2013'] = '2013-01-01,2013-12-31'
        self.terrai_periods['2014'] = '2014-01-01,2014-12-31'
        self.terrai_periods['2015'] = '2015-01-01,2015-12-31'
        self.terrai_periods['2016'] = '2016-01-01,2016-12-31'
        self.terrai_periods['2004_2016'] = '2004-01-01,2016-12-31'

        #create period dict for UMD Loss
        self.tcloss_periods = {}
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
        self.tcloss_periods['2000_2015'] = '2001-01-01,2015-12-31'

    def analyze(self, endpoint, geostore, period=None):
        '''master method to send get requests to API
        :param endpoint: api endpoint
        :param period: time period of request YYYY-MM-DD,YYYY-MM-DD
        :param geostore: unique hash assigned to geojson
        :return: response from the GFW API'''

        #Add requests cachine to speed up json requests
        requests_cache.install_cache(endpoint, backend='sqlite', expire_after=10000000)

        api_path = self.api + endpoint

        payload = {'period': period, 'geostore': geostore}

        try:
            r = requests.get(api_path, params= payload)
            print "using cache {}".format(str(r.from_cache))
            data = r.json()
            return data
        except ValueError, e:
            print "Value Error when decoding json because {}".format(str(e))

    def update_sheet(self, layer_name, layer_stats):
        '''method to update google sheet with layer_stats
        :param layer_name: the dataset of the Stats
        :param layer_stats: a dictionary of the stats'''
        #Todo add optional fields list argument

        for id, loss_dict in layer_stats.iteritems():
            for col_name, loss_val in loss_dict.iteritems():
                print "updating {0} at {1} and col {2} with {3}".format(layer_name, col_name, id, loss_val)
                try:
                    gs.set_value('Name', id, col_name, layer_name, loss_val)
                    print "{0} values set for {1} at {2}".format(layer_name, id, col_name)
                except ValueError, e:
                    print "value error for {0} because {1}".format(id, str(e))

    def download_sheet(self, layer_name):
        '''download csv by sheet
        :param layer_name: name of dataset will be name of CSV'''

        #Download spreadsheet
        csv = layer_name.replace(" ", "_")
        csv_name = csv + '_Stats'

        if layer_name == "Protected Areas":
            download_url = 'https://docs.google.com/spreadsheets/d/1uWL2xf7XNkRfqmfBeV-KtEKLky_4kVFA7dZIsBMjuB8/export?format=csv&id=1uWL2xf7XNkRfqmfBeV-KtEKLky_4kVFA7dZIsBMjuB8&gid=0'
        elif layer_name == "Forest Management Contracts":
            download_url = 'https://docs.google.com/spreadsheets/d/1uWL2xf7XNkRfqmfBeV-KtEKLky_4kVFA7dZIsBMjuB8/export?format=csv&id=1uWL2xf7XNkRfqmfBeV-KtEKLky_4kVFA7dZIsBMjuB8&gid=1463225161'
        elif layer_name == 'Community Forests':
            download_url = 'https://docs.google.com/spreadsheets/d/1uWL2xf7XNkRfqmfBeV-KtEKLky_4kVFA7dZIsBMjuB8/export?format=csv&id=1uWL2xf7XNkRfqmfBeV-KtEKLky_4kVFA7dZIsBMjuB8&gid=1516982985'

        gs.download_spreadsheet(csv_name, download_url)
