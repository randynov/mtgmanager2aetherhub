import requests
from urllib.parse import urlencode
import json
import logging
import openpyxl
import pandas as pd
import csv
from config import *
import base64
import re
import sys
import json
from ratelimit import limits
import requests


# Set logging messages
logging.basicConfig(filename='scryfall.log',
                    # format='{%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
                    format='%(levelname)s - %(message)s',
                    encoding='utf-8',
                    filemode='w',
                    level=logging.DEBUG)

"""
logging.debug('DEBUG')
logging.info('INFO')
logging.warning('WARNING')
logging.error('ERROR')
logging.critical('CRITICAL')
"""


def scryfall():
    FileMissing = (ValueError, IndexError)
    # Open CSV Input file
    try:
        file = sys.argv[1]
    except FileMissing as exc:
        sys.exit("USAGE: python scryfall.py INPUT.csv OUTPUT.csv")
    logging.debug('Input File: %s', file)
    fp = open(file)
    df = pd.read_csv(file, error_bad_lines=False).fillna("")

    # Define CSV Output file
    try:
        save_file = sys.argv[2]
    except FileMissing as exc:
        sys.exit("USAGE: python scryfall.py INPUT.csv OUTPUT.csv")
    logging.debug('Output File: %s', save_file)

    """
    Convert csv columns to dataframe with pandas
    """
    collector_number = df['collector_number']
    extras = df['extras']
    language = df['language']
    name = df['name']
    oracle_id = df['oracle_id']
    quantitie = df['quantity']
    scryfall_id = df['scryfall_id']
    set_code = df['set_code']
    set_name = df['set_name']

    data_count = df.shape[0]
    print('Cards in List: ', data_count)
    # logging.DEBUG('Cards in List: ', data_count)
    for i in range(data_count):
        if scryfall_id[i] == '':
            response, result = request_to_api(name[i], set_code[i])
            # if the status code is 200 the request is correct
            if response.status_code == 200:
                # card count
                total_cards = result['total_cards']

                # response data
                data = result['data']

                # If it returns more than 1 result, the id of the
                # result matching the card name is retrieved.
                if total_cards > 1:
                    for card in data:
                        if card['name'] == name[i]:
                            scryfall_id[i] = card['id']
                else:
                    scryfall_id[i] = data[0]['id']

                    # logging info check cards_sample.log
                    params = 'info'
                    message = 'Card found' + ' {' + \
                        'name: ' + name[i] + ', ' + \
                        'set_code: ' + set_code[i] + ', ' + \
                        'id: ' + scryfall_id[i]
                    logging.DEBUG('Card Found: %s', message)
                    print('Card Found: %s', message)
            else:
                # logging error check cards_sample.log
                params = 'error'
                message = 'Card NOT found' + ' {' + \
                    'name: ' + name[i] + ', ' + \
                    'set_code: ' + set_code[i] + ', ' + \
                    'details: ' + result['details']
                logging.INFO('Card NOT Found: %s', message)
    # save updated csv
    df.to_csv(save_file, index=False, quotechar='"', quoting=csv.QUOTE_ALL)


def request_to_api(name, set_code):
    """
    Request to scryfall api
    """
    # url encode funtion
    url = url_encode(name, set_code)
    # request to scryfall api
    response = requests.get(url)
    # convert response to json
    result = json.loads(response.text)
    return response, result


def url_encode(name, set_code):
    """
    URL correction in scryfall api format
    """
    # base url
    base_endpoint = "https://api.scryfall.com/cards/search?q="

    # query string parameters
    params = {
        "set": set_code,
        "name": name
    }

    # url encoded join parameters
    params_encoded = urlencode(params).replace(
        "+", "%20").replace("=", "%3D").replace("&", "%2B")
    detail_url = f"{base_endpoint}{params_encoded}"
    return detail_url


scryfall()
