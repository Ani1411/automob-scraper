import json
from json.decoder import NaN

with open('jsons/bikes.json') as f:
    bikes_json = json.load(f)

print(bikes_json[0].keys())

for bike in bikes_json:
    bike['short_info'] = bike['short_info'] if bike['short_info'] is not NaN else 'NA'
    bike['fuel_type'] = bike['fuel_type'] if bike['fuel_type'] is not NaN else 'NA'

with open('jsons/bikes.json', 'w') as f:
    json.dump(bikes_json, f)

with open('jsons/cars.json') as f:
    cars_json = json.load(f)

for car in cars_json:
    car['short_info'] = car['short_info'] if car['short_info'] is not NaN else 'NA'
    car['fuel_type'] = car['fuel_type'] if car['fuel_type'] is not NaN else 'NA'

with open('jsons/cars.json', 'w') as f:
    json.dump(cars_json, f)

# bikes_db_structure = {
#     'key_specs': [],
#     'colour_options_and_price_in_india': [],
#     'engine_and_gearbox': [],
#     'brakes_and_tyres': [],
#     'dimensions_and_weight': [],
#     'instrument_console_features': [],
#     'battery_and_lighting': [],
#     'comfort_features': [],
#     'suspension_and_chassis': [],
#     'technical_highlights': [],
#     'miscellaneous_information': [],
#     'maxabout_rating_and_overview': [],
#     'mileage_and_top_speed': [],
#     'key_features_and_competitors': [],
#     'performance_figures': []
# }
#
# cars_db_structure = {
#     'key_specs': [],
#     'quick_facts_and_information': [],
#     'engine_and_transmission': [],
#     'performance_and_mileage': [],
#     'dimensions_and_weight': [],
#     'capacity': [],
#     'brakes_and_suspension': [],
#     'wheels_and_tyres': [],
#     'comfort_and_convenience': [],
#     'exterior_features': [],
#     'interior_features': [],
#     'active_and_passive_safety_features': [],
#     'braking_and_traction': [],
#     'locks_and_security': [],
#     'instrumentation': [],
#     'lighting': [],
#     'infotainment': [],
#     'seats_and_upholstery': [],
#     'key_features_of_the_car': []
# }
#
# for row in bikes:
#     keys = row.keys()
#     for key in keys:
#         if key not in ['name', 'hero_img_link', 'vehicle_photos', 'price']:
#             bikes_db_structure[key].extend(row[key].keys())
#             bikes_db_structure[key] = list(set(bikes_db_structure[key]))
#
#
# for row in cars:
#     keys = row.keys()
#     for key in keys:
#         if key not in ['name', 'hero_img_link', 'vehicle_photos', 'price']:
#             cars_db_structure[key].extend(row[key].keys())
#             cars_db_structure[key] = list(set(cars_db_structure[key]))
#
# bikes_key = bikes_db_structure.keys()
# cars_key = cars_db_structure.keys()
#
# for key in bikes_key:
#     bikes_db_structure[key] = sorted(bikes_db_structure[key])
#
# for key in cars_key:
#     cars_db_structure[key] = sorted(cars_db_structure[key])
#
# with open('jsons/bikes_db.json', 'w') as f:
#     json.dump(bikes_db_structure, f)
#
# with open('jsons/cars_db.json', 'w') as f:
#     json.dump(cars_db_structure, f)
