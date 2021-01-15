import requests
from bs4 import BeautifulSoup

def remove_items(test_list, item): 
      
    # using list comprehension to perform the task 
    res = [i for i in test_list if i != item] 
  
    return res 
def get_car_variants(url):
    dict_car_variants = {}
    price_list = []
    final_dict = {}
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='alltab')
    car_v_names = results.find_all('a')
    car_v_specs = results.find_all('ul', class_ = 'feature-list')
    car_v_prices = results.find_all('p', class_ = 'price-txt')
    for car_v_name, car_v_spec in zip(car_v_names, car_v_specs):
        car_v_name_text = car_v_name.text
        car_v_spec_dirty = car_v_spec.text
        dict_car_variants[car_v_name_text] = car_v_spec_dirty
    for i in car_v_prices:
        text = i.text
        price_list.append(text)
    list_price_ex_showroom = price_list[::2]
    list_price_on_road = price_list[1::2] 
    dict_car_prices = dict(zip(list_price_ex_showroom, list_price_on_road))
    dict_ex_showroom_prices = dict(zip(dict_car_variants.keys(), dict_car_prices.keys()))
    dict_on_road_prices = dict(zip(dict_car_variants.keys(), dict_car_prices.values()))
    for key, value in zip(dict_car_variants.keys(), dict_car_variants.values()):
        ex_showroom = []
        on_road = []
        spec_list_temp = tuple(str(value).split())
        price_list_temp_ex_showroom = tuple(str(dict_ex_showroom_prices[key]).split())
        if 'Crore' in price_list_temp_ex_showroom:
            price_list_final_ex_showroom = tuple(remove_items(
                                                    remove_items(
                                                        remove_items(
                                                            remove_items(
                                                                remove_items(price_list_temp_ex_showroom, 'Crore'), 
                                                                '₹'), 
                                                                'Lakhs'), 
                                                                '-'), 
                                                                ' '))
            for item in price_list_final_ex_showroom:
                item_float = float(item)*100
                ex_showroom.append(item_float)
                tuple_ex_showroom = tuple(ex_showroom)
        else:
            price_list_final_ex_showroom = tuple(remove_items(
                                                    remove_items(
                                                        remove_items(
                                                            remove_items(
                                                                remove_items(price_list_temp_ex_showroom, 'Crore'), 
                                                                '₹'), 
                                                                'Lakhs'), 
                                                                '-'), 
                                                                ' '))
            tuple_ex_showroom = price_list_final_ex_showroom 
        price_list_temp_on_road = tuple(str(dict_on_road_prices[key]).split())
        if 'Crore' in price_list_temp_on_road:
            price_list_final_on_road = tuple(remove_items(
                                                    remove_items(
                                                        remove_items(
                                                            remove_items(
                                                                remove_items(price_list_temp_ex_showroom, 'Crore'), 
                                                                '₹'), 
                                                                'Lakhs'), 
                                                                '-'), 
                                                                ' '))
            for item in price_list_final_on_road:
                item_float = float(item)*100
                on_road.append(item_float)
                tuple_on_road = tuple(on_road)
        else:
            price_list_final_on_road = tuple(remove_items(
                                                remove_items(
                                                    remove_items(
                                                        remove_items(
                                                            remove_items(price_list_temp_on_road, 'Crore'), 
                                                            '₹'), 
                                                            'Lakhs'), 
                                                            '-'), 
                                                            ' '))
            tuple_on_road = price_list_final_on_road
        try:
            final_dict[key] = { 'FuelType' : spec_list_temp[0], 
                            'Enginedisplacement' : spec_list_temp[1], 
                            'Transmission' : spec_list_temp[2], 
                            'MaximumPower(ps)' : spec_list_temp[3], 
                            'Mileage' : spec_list_temp[4], 
                            'Ex-Showroom Price Delhi' : tuple_ex_showroom[0],
                            'Ex-Showroom Price Mumbai' : tuple_ex_showroom[1],
                            'Ex-Showroom Price Kolkata' : tuple_ex_showroom[2],
                            'Ex-Showroom Price Chennai' : tuple_ex_showroom[3],
                            'On-Road Price Delhi' : tuple_on_road[0],
                            'On-Road Price Mumbai' : tuple_on_road[1],
                            'On-Road Price Kolkata' : tuple_on_road[2],
                            'On-Road Price Chennai' : tuple_on_road[3]
                            }
        except IndexError:
            final_dict[key] = { 'FuelType' : spec_list_temp[0], 
                            'Enginedisplacement' : spec_list_temp[1], 
                            'Transmission' : spec_list_temp[2], 
                            'MaximumPower(ps)' : spec_list_temp[3],
                            'Ex-Showroom Price Delhi' : tuple_ex_showroom[0],
                            'Ex-Showroom Price Mumbai' : tuple_ex_showroom[1],
                            'Ex-Showroom Price Kolkata' : tuple_ex_showroom[2],
                            'Ex-Showroom Price Chennai' : tuple_ex_showroom[3],
                            'On-Road Price Delhi' : tuple_on_road[0],
                            'On-Road Price Mumbai' : tuple_on_road[1],
                            'On-Road Price Kolkata' : tuple_on_road[2],
                            'On-Road Price Chennai' : tuple_on_road[3]
                            }
    return final_dict
print(get_car_variants('https://www.overdrive.in/cars/aston-martin/db11-m537/'))