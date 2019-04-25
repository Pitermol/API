import requests
import sys
from bolder import bolder
from geocode_search import geocode_search
from flask import Flask, request
import logging
import json
# если бы такое обращение, например, произошло внутри модуля logging, то мы бы получили 'logging'
app = Flask(__name__)

# Устанавливаем уровень логирования
logging.basicConfig(level=logging.INFO)

# Создадим словарь, чтобы для каждой сессии общения с навыком хранились подсказки, которые видел пользователь.
# Это поможет нам немного разнообразить подсказки ответов (buttons в JSON ответа).
# Когда новый пользователь напишет нашему навыку, то мы сохраним в этот словарь запись формата
# sessionStorage[user_id] = { 'suggests': ["Не хочу.", "Не буду.", "Отстань!" ] }
# Такая запись говорит, что мы показали пользователю эти три подсказки. Когда он откажется купить слона,
# то мы уберем одну подсказку. Как будто что-то меняется :)


@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info('Request: %r', response)
    return json.dumps(response)


def handle_dialog(res, req):
    user_id = req['session']['user_id']
    if req['session']['new']:
        res['response']['text'] = \
            'Привет! Я могу сравнить города!'
        return
    # Получаем города из нашего

    cities = req['request']['original_utterance'].lower().split()
    search_api_server = "https://search-maps.yandex.ru/v1/"
    text = [cities[i + 1] for i in range(int(cities[0]))]
    circle = [i for i in cities[int(cities[0]) + 2:]]

    org = []
    for i in circle:
        for g in text:
            address_ll = geocode_search(i)
            search_params = {
                "apikey": 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3',
                "text": g,
                "lang": "ru_RU",
                "ll": address_ll,
                "spn": 0.002,
                "type": "biz",
                "results": 25
            }

            response = requests.get(search_api_server, params=search_params)
            if not response:
                pass
            json_response = response.json()


            # print(search_params['ll'])
            # print(search_params['spn'])
            organization1 = json_response["features"]
            organization11 = []


            #res['response']['text'] = '6'
            #return
            for o in organization1:
                if o['properties']['CompanyMetaData']['name'] not in organization11:
                    organization11.append(o['properties']['CompanyMetaData']['name'])
            organization1 = organization11[:]

            # ... и выполняем запрос
            org.append(str(len(organization1)))
    iop = ''
    for i in range(len(circle)):
        for j in range(len(text)):
            iop += circle[i] + ',' + text[j] + ':' + org[i * len(circle) + j]
    res['response']['text'] = iop


def get_cities(req):
    cities = []
    for entity in req['request']['nlu']['entities']:
            cities.append(entity)
    return cities


if __name__ == '__main__':
    app.run()