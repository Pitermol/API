import requests
import sys
from bolder import bolder
from geocode_search import geocode_search
search_api_server = "https://search-maps.yandex.ru/v1/"
text = [input() for _ in range(int(input()))]
circle = [input() for _ in range(int(input()))]
org = []
r=[]
for i in circle:
    for g in text:
        address_ll = geocode_search(i)
        search_params = {
            "apikey": 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3',
            "text": g,
            "lang": "ru_RU",
            "ll": address_ll,
            "spn": bolder(i),
            "type": "biz",
            "results": 500
        }
        response = requests.get(search_api_server, params=search_params)
        if not response:
            pass
        json_response = response.json()

        # print(search_params['ll'])
        # print(search_params['spn'])
        organization1 = json_response["features"]
        organization11 = []
        delta = "0.005"
        for o in organization1:
            if o['properties']['CompanyMetaData']['name'] not in organization11:
                organization11.append(o['properties']['CompanyMetaData']['name'])
        organization1 = organization11[:]

        # Собираем параметры для запроса к StaticMapsAPI:
        map_params = {
            # позиционируем карту центром на наш исходный адрес
            "ll": address_ll,
            # Радиус поиска
            "spn": ",".join([delta, delta]),
            # центр поиска
            "l": "map",
        }

        map_api_server = "http://static-maps.yandex.ru/1.x/"
        # ... и выполняем запрос
        response = requests.get(map_api_server, params=map_params)
        org.append(str(len(organization1)))
for i in range(len(circle)):
    for j in range(len(text)):
        print(circle[i] + ',', text[j] + ':', org[i * len(circle) + j])