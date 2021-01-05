import requests
from urllib.parse import urlencode
import json
import logging
import openpyxl
import pandas as pd
import csv
from config import *
import base64
from selenium import webdriver
from time import sleep
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
import json


def scryfall():
    # read csv file
    df = pd.read_csv(csv_file, error_bad_lines=False).fillna(
        "")
    """"
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
    for i in range(data_count):
        if scryfall_id[i] == '':
            r, result = request_to_api(name[i], set_code[i])
            # if the status code is 200 the request is correct
            if r.status_code == 200:
                # card count
                total_cards = result['total_cards']
                # response data
                data = result['data']

                # If it returns more than 1 result, the id of the
                # result matching the card name is retrieved.
                if total_cards > 1:
                    for j in data:
                        if j['name'] == name[i]:
                            scryfall_id[i] = j['id']
                else:
                    scryfall_id[i] = data[0]['id']

                    # logging info check cards_sample.log
                    params = 'info'
                    message = 'Card found' + \
                        ' {' + 'name: ' + name[i] + ', ' + 'set_code: ' + \
                        set_code[i] + ', ' + 'id: ' + scryfall_id[i]
                    save_log(message, params)  # save_log function
                    print('Card found:', name[i])
            else:
                # logging error check cards_sample.log
                params = 'error'
                message = 'Card not found' + \
                    ' {' + 'name: ' + name[i] + ', ' + 'set_code: ' + \
                    set_code[i] + ', ' + 'details: ' + result['details']
                save_log(message, params)  # save_log function
                print('Card not found...')

    df.to_csv('cards-sample.csv', index=False, quotechar='"',
              # save updated csv
              quoting=csv.QUOTE_ALL)


def request_to_api(name, set_code):
    """
    Request to scryfall api
    """
    # url encode funtion
    url = url_encode(name, set_code)
    # request to scryfall api
    r = requests.get(url)
    # convert response to json
    result = json.loads(r.text)
    return r, result


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


def save_log(message, params):
    """
    Save log information and error info
    """
    logger = logging.getLogger(__name__)
    # set log level
    logger.setLevel(logging.INFO)

    # create file handler
    handler = logging.FileHandler('cards_sample.log')
    handler.setLevel(logging.INFO)

    # create logging format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # save handler to logger
    logger.addHandler(handler)

    logger.info(message) if params == 'info' else logger.error(message)
    # %%
