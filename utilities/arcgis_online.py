import requests
import json
import os
from ConfigParser import ConfigParser

import util

def request_token(agol_creds):
    '''
    :param agol_creds: the name of the local file with the user/pass
    :return: a dictionary with folder_name, folder_id, item_name, item_id
    '''

    user = util.get_token(agol_creds)[0][1]
    password = util.get_token(agol_creds)[1][1]

    d = {"username": user,
         "password": password,
         "referer":"http://www.arcgis.com",
         "f": "json"}

    url = "https://www.arcgis.com/sharing/rest/generateToken"

    r = requests.post(url, data = d)

    response = json.loads(r.content)
    token = response['token']

    if 'error' in response.keys():
        raise Exception(response['message'], response['details'])

    return token

def update_feature_service(layer_name):
    '''overwrite csv feature servics in agol with new data in output folder
    :param layer_name: name of dataset'''
    #https://gis.stackexchange.com/questions/208763/overwrite-feature-class-in-arcgis-online-using-python

    #specify update csv
    csv = layer_name.replace(" ", "_")
    csv_name = csv + '_Stats'

    f = os.path.dirname(os.getcwd()) + '/output' + '/' + csv_name + '.csv'

    #Set variables: token, base url, foder and item id
    token = request_token()

    base_url = "https://www.arcgis.com/sharing/rest"

    folder_id = 'faf309bb63c647d0a28d7116f03fba4e'

    if layer_name == 'Protected Areas':
        agol_id = '980d2596c7b34a6bb666e0070bf72b25'
    elif layer_name == 'Forest Management Contracts':
        agol_id = 'bdd1024ad1e6497fa532734c594002fd'

    #specify post operation variables: url, payload
    url = '{0}/content/users/{1}/{2}/items/{3}/update'.format(base_url, 'LiberiaForests',
                                                              folder_id, agol_id)

    d = {"overwrite": "true",
            "token" :token,
            "f":"json"}

    #make post request
    r = requests.post(url, data = d, files = f)
    response = json.loads(r.content)

    print response
