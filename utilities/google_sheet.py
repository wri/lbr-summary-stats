import json
import gspread
import os
import logging
import requests
from oauth2client.service_account import ServiceAccountCredentials

#https://docs.google.com/spreadsheets/d/1uWL2xf7XNkRfqmfBeV-KtEKLky_4kVFA7dZIsBMjuB8/edit?usp=sharing

def _open_spreadsheet(sheet_name, custom_key=False):
    """
    Open the spreadsheet for read/update
    :return: a gspread wks object that can be used to edit/update a given sheet
    """

    #path to Oauth json creds
    spreadsheet_file = os.getcwd() + r"/tokens/spreadsheet.json"

    if custom_key:
        spreadsheet_key = custom_key
    else:
        spreadsheet_key = r'1uWL2xf7XNkRfqmfBeV-KtEKLky_4kVFA7dZIsBMjuB8'

    # Updated for oauth2client
    # http://gspread.readthedocs.org/en/latest/oauth2.html
    credentials = ServiceAccountCredentials.from_json_keyfile_name(spreadsheet_file,
                                                                   ['https://spreadsheets.google.com/feeds'])

    gc = gspread.authorize(credentials)
    wks = gc.open_by_key(spreadsheet_key).worksheet(sheet_name)

    return wks

def get_value(unique_id_col, unique_id_value, colname, sheet_name, spreadsheet_key=None):
    """
    Update a value in the spreadsheet given the layername and column name
    :param unique_id_col: the column that has unique ids (tech_title in the config table)
    :param unique_id_value: the particular value we're looking for in the unique id col
    :param colname: the column name to get the value of
    :param sheet_name: the name of the sheet in the google doc
    :param spreadsheet_key: key for the spreadsheet if not the default config table
    """

    wks, row_id, col_id = get_cell_location(unique_id_col, unique_id_value, colname, sheet_name, spreadsheet_key)

    return wks.cell(row_id, col_id).value


def get_cell_location(unique_id_col, unique_id_value, colname, sheet_name, spreadsheet_key=None):
    """
    Get the row and col of a particular cell so later we can report the value or update it
    :param unique_id_col: the column that has unique ids (tech_title in the config table)
    :param unique_id_value: the particular value we're looking for in the unique id col
    :param colname: the column name to get the value of
    :param sheet_name: the name of the sheet in the google doc
    :param spreadsheet_key: json key if not the default config table
    """

    wks = _open_spreadsheet(sheet_name, spreadsheet_key)

    gdoc_as_lists = wks.get_all_values()

    unique_id_index = gdoc_as_lists[0].index(unique_id_col)

    row_id = [x[unique_id_index] for x in gdoc_as_lists].index(unique_id_value) + 1
    col_id = gdoc_as_lists[0].index(colname) + 1

    return wks, row_id, col_id

def set_value(unique_id_col, unique_id_value, colname, sheet_name, in_update_value, spreadsheet_key=None):
    """
    Update a value in the spreadsheet given the layername and column name
    :param unique_id_col: the column that has unique ids
    :param unique_id_value: the particular value we're looking for in the unique id col
    :param colname: the column name to update
    :param sheet_name: the name of the sheet to update
    :param in_update_value: the value to set
    :param spreadsheet_key: key for the spreadsheet if not the default config table
    """

    wks, row_id, col_id = get_cell_location(unique_id_col, unique_id_value, colname, sheet_name, spreadsheet_key)

    wks.update_cell(row_id, col_id, in_update_value)

def update_gs_timestamp(layername, gfw_env):
    """
    Update the 'last_updated' column for the layer specified with the current date
    :param layername: the row to update (based on tech_title column)
    :param gfw_env: gfw env
    """
    set_value('tech_title', layername, 'last_updated', gfw_env, time.strftime("%m/%d/%Y"))

    # If the layer is part of a global_layer, update its last_updated timestamp as well
    associated_global_layer = get_layerdef(layername, gfw_env)['global_layer']

    if associated_global_layer:
        set_value('tech_title', associated_global_layer, 'last_updated', gfw_env, time.strftime("%m/%d/%Y"))

def download_spreadsheet(layer_name, url):

    r = requests.get(url)
    assert r.status_code == 200, 'Wrong status code'

    output_dir = os.getcwd() + r"/output"

    with open(os.path.join(output_dir, layer_name + '.csv'), 'wb') as f:
        f.write(r.content)

    print "%s csv downloaded" %(layer_name)
