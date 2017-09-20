import requests
import json
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

    print token
    return token
