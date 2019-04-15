import requests
import sys
from geocode import geocode
from bolder import bolder
from geocode_search import geocode_search
search_api_server = "https://search-maps.yandex.ru/v1/"
text = 'аптека'
circle = 'Москва'
address_ll = geocode_search(circle)
search_params = {
    "apikey": 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3',
    "text": text,
    "lang": "ru_RU",
    "ll": address_ll,
    "spn": bolder(circle),
    "type": "biz"
}
response = requests.get(search_api_server, params=search_params)
if not response:
    pass
json_response = response.json()

# Получаем первую найденную организацию.
organization = json_response["features"]
# Название организации.
#org_name = organization["properties"]["CompanyMetaData"]["name"]
# Адрес организации.
#org_address = organization["properties"]["CompanyMetaData"]["address"]

# Получаем координаты ответа.
#point = organization["geometry"]["coordinates"]
#org_point = "{0},{1}".format(point[0], point[1])
delta = "0.005"


# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    # позиционируем карту центром на наш исходный адрес
    "ll": address_ll,
    "spn": ",".join([delta, delta]),
    "l": "map",
    # добавим точку, чтобы указать найденную аптеку
#    "pt": "{0},pm2dgl".format(org_point)
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)
print(organization)
#print(org_name)