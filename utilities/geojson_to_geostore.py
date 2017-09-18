import requests
import json

def get_geojsons(layer_name):

    #specify query url to dataset in ArcGIS Open data site
    if layer_name == "Protected Areas":
        geojson_url = "https://opendata.arcgis.com/datasets/2df3e0af67af40e08ed0f6af11f34e5c_0.geojson"
    elif layer_name == "Community Forests":
        geojson_url = "https://opendata.arcgis.com/datasets/b403afe5eb8e46799fe36b6ed459770c_0.geojson"
    elif layer_name == "Forest Management Contracts"
        geojson_url = "https://opendata.arcgis.com/datasets/0a1d9fe0749f4be29029dc8f9e932668_0.geojson"
    else:
        raise KeyError("layer_name does not exist")

    geojson = requests.get(geojson_url)

    data = geojson.json()

    return data

def create_geostore_dict(layer_name):
    '''create geostoreID from geojson by sending post request to API'''

    #geostore dict will hold data name and geostore id
    geostore_dict = {}

    #path to geostore microservice
    api_path = "https://production-api.globalforestwatch.org/geostore"

    #get geojson
    geojson = get_geojsons(layer_name)

    #create dict
    for x in range (0, len(geojson['features'])):
        geometry = geojson['features'][x]['geometry']
        payload = {"geojson": geojson}
        r = requests.post(api_path, json=payload)
        geostore_id = r.json()["data"]["id"]
        geostore_dict[geojson['features'][x]['properties']['NAME']] = geostore_id

    return geostore_dict
