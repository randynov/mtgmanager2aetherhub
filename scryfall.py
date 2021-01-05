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


"""
def github_commit():
    url = f'https://api.github.com/repos/{branch_github_user_name}/{github_repo_name}/contents/{csv_file}?access_token=' + github_token
    r = requests.get(url)
    # target repo sha
    sha = r.json()['sha']

    with open(csv_file, 'rb') as f:
        content = str(base64.b64encode(f.read()), encoding='utf8')
        data = {'message': message, 'content': content,
                'sha': sha, 'branch': 'main'}
        r_to_github = requests.put(url, json=data)

def github_pull_request():
    # github changes pull request to
    browserProfile = webdriver.FirefoxProfile()
    options = FirefoxOptions()
    browserProfile.set_preference("intl.accept_languages", "en-us")
    options.add_argument("--headless")
    browserProfile.set_preference(
        "general.useragent.override", "Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166")
    browser = webdriver.Firefox(options=options, firefox_profile=browserProfile,
                                executable_path=GeckoDriverManager().install())

    browser.get("https://github.com/login")
    sleep(2)
    # Github login process
    username_input = browser.find_element_by_id("login_field")
    password_input = browser.find_element_by_id("password")

    username_input.send_keys(branch_github_user_name)
    password_input.send_keys(password)
    password_input.send_keys(Keys.ENTER)
    sleep(2)
    # redirect pull request page
    browser.get(
        f"https://github.com/{branch_github_user_name}/{github_repo_name}/pulls")
    sleep(2)
    browser.get(
        f"https://github.com/{github_username}/{github_repo_name}/compare/{branch_name}...{branch_github_user_name}:main")

    sleep(2)
    try:
        browser.find_element_by_xpath(
            "/html/body/div[4]/div/main/div[2]/div/div[4]/div/button").click()
    except:
        browser.find_element_by_xpath(
            "/html/body/div[4]/div/main/div[2]/div/div[4]/div/button").click()
    sleep(2)
    try:
        browser.find_element_by_xpath(
            "//*[@id='new_pull_request']/div/div[1]/div/div[2]/div[2]/div/button").click()
    except:
        browser.find_element_by_xpath(
            "//*[@id='new_pull_request']/div/div[1]/div/div[2]/div[2]/div/button").click()


if __name__ == '__main__':
    scryfall()
    github_commit()
"""
