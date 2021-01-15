import collections
import requests
from bs4 import BeautifulSoup
import functions
import json
import time
start_time = time.time()
url = 'https://www.overdrive.in/cars/brands/'
specs = {}
data = {}
brand_by_cars = {}
data_final = collections.defaultdict(list)
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find(id='app')

brand_names_temp = results.find_all('div', class_='block-cell')
for brand_names in brand_names_temp:
    brand_link = brand_names.find('a')['href']
    brand_name = brand_names.find('img')['alt']
    data[brand_name] = brand_link
for key, value in zip(data.keys(), data.values()):
    temp_dict = functions.get_car_by_brand(value)
    brand_by_cars[key] = temp_dict
    for key1, value1 in zip(temp_dict.keys(), temp_dict.values()):
        specs[key1] = functions.get_car_details(value1)
        try:
            data_final[key].append({key1: specs[key1], 'Variants' : functions.get_car_variants(value1)})
        except KeyError:
            try:
                data_final[key] = {key1 : specs[key1], 'Variants' : functions.get_car_variants(value1)}
            except KeyError:
                pass
        except IndexError:
            pass
json_data = json.dumps(data_final, sort_keys=True, indent=4)
with open ('output.json', 'w') as file:
    file.write(json_data)
time_ = time.time() - start_time
print('Took {} Minutes and {} Seconds'.format(time_//60, time_%60))