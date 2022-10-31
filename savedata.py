import json

import pandas as pd
import requests

# df = pd.read_csv('csvs/companies.csv')
# df = df.fillna('')
#
# data = df.to_dict(orient='records')
#
# response = requests.post('http://127.0.0.1:8000/api/companies/post', json=data)
# print(response.json())


# df = pd.read_csv('csvs/details.csv')
# df = df.fillna('')
#
# data = df.to_dict(orient='records')
#
# response = requests.post('http://127.0.0.1:8000/api/models/post/', json=data)
# print(response.json())


models_df = pd.read_csv('csvs/api.vehiclemodels.csv')
models_df = models_df[['id', 'model', 'company_id']]
models = models_df.to_dict(orient='records')
# models = requests.get('http://127.0.0.1:8000/api/models/all/').json()['result']

with open('jsons/bikes.json') as f:
    s_json = json.load(f)

for car in s_json:
    for var in models:
        k = f"{' '.join(var['company_id'].split()[:-1])} {var['model']}"
        if car['model_name'] == k:
            if 'DIMENSIONS & WEIGHT' in car['details_n_specs'].keys():
                dnw = car['details_n_specs']['DIMENSIONS & WEIGHT']
                if "Turning Radius" in dnw.keys():
                    dnw["Turning Radius"] = dnw["Turning Radius"].replace('\u0000', '')
            car['model'] = var['id']

with open('jsons/bikes.json', 'w') as f:
    json.dump(s_json, f)
#
response = requests.post('http://127.0.0.1:8000/api/variants/post/', json=s_json)
print(response.text)
