import requests


def geocode(address):
    """ первый топоним из ответа геокодера """
    # Собираем запрос для геокодера.
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {"geocode": address, "format": "json"}

    # Выполняем запрос.
    response = None
    try:
        response = requests.get(geocoder_api_server, params=geocoder_params)
        if response:
            # Преобразуем ответ в json-объект
            json_response = response.json()

            # Получаем первый топоним из ответа геокодера.
            # Согласно описанию ответа он находится по следующему пути:
            return json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        else:
            print("Ошибка выполнения запроса:")
            print(geocoder_api_server, params=geocoder_params)
            print("Http статус:", response.status_code, "(", response.reason, ")")
    except:
        print("Запрос не удалось выполнить. Проверьте подключение к сети Интернет.")




# print("В файле 'f_json.json' ответ на запрос", geocode('Москва, ул. Ак. Королева, 12'))