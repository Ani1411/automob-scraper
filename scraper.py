import contextlib
import json
import time

import numpy as np
import requests as requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium import webdriver


def get_url_response(url):
    response = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})
    return BeautifulSoup(response.content, 'html.parser'), response.status_code, response.url


def get_all_company_links(company_type):
    url = f'https://autos.maxabout.com/{company_type}/companies'
    page_html, status, current_url = get_url_response(url)
    company_divs = page_html.findAll('div', class_='companies')
    company_data = []

    for div in company_divs:
        link = div.find("a")['href'] if div.find("a") else ''
        title = div.find("a")['title'] if div.find("a") else ''
        logo_img = div.find('img')['data-original'][:-8] if div.find('img') else ''
        company_name = div.find('div', class_='info').text if div.find('div', class_='info') else ''
        model_count = div.find('div', class_='info muted').text.split(' ')[0] if div.find('div',
                                                                                          class_='info muted') else ''
        data = {
            'link': link,
            'title': title,
            'logo_img': logo_img,
            'company_name': company_name,
            'model_count': model_count
        }
        company_data.append(data)

    for veh in tqdm(company_data):
        page_html, status, current_url = get_url_response(veh['link'])
        try:
            about_div = page_html.find('div', class_='para')
            veh['about'] = about_div.text.replace('\n', ' ').replace('\"', '').replace('\'', ' ')
        except Exception:
            veh['about'] = ''

    company_data_df = pd.DataFrame(company_data)
    company_data_df.to_csv(f'csvs/{company_type}_company_data.csv', index=False)


# get_all_company_links('cars')
# get_all_company_links('bikes')


def get_vehicle_list(veh_type):
    vehicles_df = pd.read_csv(f'csvs/company_data_{veh_type}.csv')
    vehicles_list = vehicles_df.to_dict(orient='records')
    # url_list = vehicles_df['link'].to_list()
    vehicle_details = []
    for vehicle in tqdm(vehicles_list):
        html, status, current_url = get_url_response(vehicle['link'])
        if current_url == vehicle['link']:
            sections = html.findAll('div', class_="models-list boxed foreground")
            for section in sections:
                if section.find('h2') and \
                        section.find('h2').text.lower() == f"all {veh_type} by {vehicle['company_name'].lower()}":
                    if tab_pane := section.find('div', id='available'):
                        tab_anchor = tab_pane.findAll('a')
                        tab_div = tab_pane.findAll('div', class_='price text-info')
                        for anchor, div in zip(tab_anchor, tab_div):
                            vehicle['model_img'] = anchor.find('img')['data-original']
                            vehicle['model_link'] = anchor['href']
                            vehicle['model_name'] = anchor.find('b').text
                            div_text = div.text.replace('\n', '')
                            vehicle['price_range'] = div_text[div_text.index('week') + 4:]
                            vehicle_details.append(vehicle.copy())
    vehicle_details_df = pd.DataFrame(vehicle_details)
    vehicle_details_df.drop_duplicates(subset=['model_link'], keep='last', inplace=True)
    vehicle_details_df.to_csv(f'csvs/{veh_type}_details.csv', index=False)


# get_vehicle_list(veh_type='bikes')
# get_vehicle_list(veh_type='cars')


def initiate_browser(driver_path='browserdriver/geckodriver'):
    options = Options()
    options.add_argument('--start-maximized')
    browser = webdriver.Firefox(options=options, executable_path=driver_path)
    # browser = webdriver.Chrome(options=options, executable_path=self.chrome_path)
    wait = WebDriverWait(browser, 5)
    print('connected chrome urlFetch')
    return browser, wait


def get_variant_urls(veh_type):
    browser, wait = initiate_browser()
    veh_df = pd.read_csv(f'csvs/{veh_type}_details.csv')
    veh_df = veh_df[~veh_df['price_range'].isin([None, np.NaN, 'NA '])]
    all_variants = []
    for veh in tqdm(veh_df.to_dict('records')):
        veh_details = {
            'company_name': veh['company_name'],
            'sub_company': veh['title'],
            'model_link': veh['model_link'],
            'model_name': veh['model_name'],
        }
        browser.get(veh['model_link'])
        if veh['model_link'] == browser.current_url:
            wait.until(EC.presence_of_element_located((By.ID, 'VehicleInfoTabs')))
            try:
                variant_tab = wait.until(EC.presence_of_element_located((By.XPATH, '//a[@href="#relatedVariants"]')))
                variant_tab.click()
                with contextlib.suppress(Exception):
                    variant_box = wait.until(EC.presence_of_element_located((By.ID, 'other-variants')))
                    anchor = variant_box.find_element(By.CLASS_NAME, 'viewAll')
                    anchor.click()
                variant_ul = browser.find_element(By.CLASS_NAME, 'variants')
                variant_list = variant_ul.find_elements(By.TAG_NAME, 'li')

                for li in variant_list:
                    a = li.find_element(By.TAG_NAME, 'a')
                    veh_details['variant_link'] = a.get_attribute('href')
                    veh_details['variant_name'] = a.text

                    variant_info = li.find_element(By.CLASS_NAME, 'variant-info')
                    veh_details['variant_info'] = variant_info.text

                    variant_fuel = li.find_element(By.CLASS_NAME, 'variant-fuel')
                    veh_details['variant_fuel_type'] = variant_fuel.text

                    price = li.find_element(By.CLASS_NAME, 'text-info')
                    veh_details['price'] = price.text

                    all_variants.append(veh_details.copy())
            except Exception as e:
                veh_details['variant_link'] = veh['model_link']
                veh_details['variant_name'] = veh['model_name']
                all_variants.append(veh_details.copy())

    df = pd.DataFrame(all_variants)
    df.to_csv(f'csvs/{veh_type}_variant_details.csv', index=False)
    browser.quit()


# get_variant_urls(veh_type='bikes')
# get_variant_urls(veh_type='cars')


def replace_key_characters(string):
    string = string.lower().replace('-', '_').replace(' ', '_').replace('(', '_').replace(')', '_')
    return string.replace('?', '').replace('&', 'and').replace('\'', '').replace('–', '_').replace('.', '_')


def get_vehicle_specs(veh_type):
    vehicles_df = pd.read_csv(f'csvs/{veh_type}_variant_details.csv')
    vehicles_list = vehicles_df.to_dict(orient='records')
    # url_list = vehicles_df['link'].to_list()
    vehicle_details = []
    keys_list = []
    title_list = []
    for vehicle in tqdm(vehicles_list):
        html, status, current_url = get_url_response(vehicle['variant_link'])
        vehicle_obj = {
            'name': vehicle['variant_name'],
            'short_info': vehicle['variant_info'],
            'fuel_type': vehicle['variant_fuel_type'],
            'src_link': vehicle['variant_link'],
            'model_name': vehicle['model_name'],
            'hero_img_link': html.find('img', id='veh-img')['data-original']
        }
        try:
            all_img = html.findAll('img', class_='vehicle-media-img')
            vehicle_obj['vehicle_photos'] = [img['data-original'] for img in all_img]
        except Exception as e:
            print(e)
            vehicle_obj['vehicle_photos'] = []

        price_el = html.find('div', class_='vehicle-price text-info').text.replace('\n', '').replace(' ', '')
        vehicle_obj['price'] = price_el

        key_features_div = html.find('div', id='key-features')
        specs_label = key_features_div.findAll('td', class_='specs-label')
        specs_value = key_features_div.findAll('td', class_='specs-value')
        vehicle_obj['key_specs'] = {
            key.text: value.text for key, value in zip(specs_label, specs_value)
        }
        vehicle_obj['details_n_specs'] = {}

        vehicle_specs_rows = html.find('div', id='veh-details').findAll('tr')

        specs_key = ''
        for row in vehicle_specs_rows:
            td = row.findAll('td')
            if len(td) == 1:
                specs_key = row.find('h5').text
                vehicle_obj['details_n_specs'][specs_key] = {}
                title_list.append(specs_key)
            else:
                specs_label = row.find('td', class_='specs-label').text
                specs_value = row.find('td', class_='specs-value')
                keys_list.append(specs_label)
                try:
                    icon_div = specs_value.find('div', class_='icon')
                    vehicle_obj['details_n_specs'][specs_key][specs_label] = 'icon-check-mark' in icon_div['class']
                except Exception as e:
                    vehicle_obj['details_n_specs'][specs_key][specs_label] = specs_value.text
        vehicle_details.append(vehicle_obj)

    with open(f'jsons/{veh_type}.json', 'w') as f:
        json.dump(vehicle_details, f)


st = time.time()
get_variant_urls(veh_type='bikes')
et = time.time()
elapsed_time = et - st
print('Execution time:', elapsed_time, 'seconds')

st = time.time()
get_variant_urls(veh_type='cars')
et = time.time()
elapsed_time = et - st
print('Execution time:', elapsed_time, 'seconds')

st = time.time()
get_vehicle_specs(veh_type='cars')
et = time.time()
elapsed_time = et - st
print('Execution time:', elapsed_time, 'seconds')

st = time.time()
get_vehicle_specs(veh_type='bikes')
et = time.time()
elapsed_time = et - st
print('Execution time:', elapsed_time, 'seconds')
