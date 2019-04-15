import sys
import pygame
import requests
import os


def bolder(address):
    from geocode import geocode
    """ координаты объекта по его адресу
    обращаемся к функции geocode из файла geocode.py"""
    toponym = geocode(address)
    if toponym:
        # Рамка вокруг объекта:
        envelope = toponym["boundedBy"]["Envelope"]

        # левая, нижняя, правая и верхняя границы из координат углов:
        l, b = envelope["lowerCorner"].split(" ")
        r, t = envelope["upperCorner"].split(" ")

        # Вычисляем полуразмеры по вертикали и горизонтали
        dx = abs(float(l) - float(r)) / 2.0
        dy = abs(float(t) - float(b)) / 2.0

        return str(max(dx, dy))
    return None


def show_map(lon_lat=None, delta=0.005, map_type='map', pt=None):
    """ Статическая картинка в PyGame по координатам """
    # Собираем запрос для статик карт.
    map_api_server = "http://static-maps.yandex.ru/1.x/"

    toponym_longitude, toponym_lattitude = lon_lat.split(" ")
    if pt:
        pt = ",".join([toponym_longitude, toponym_lattitude])
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([delta, delta]),
        "l": map_type,
        "pt": pt
    }

    # Выполняем запрос.
    response = None
    try:
        response = requests.get(map_api_server, params=map_params)
        if response:
            # Запишем полученное изображение в файл.
            map_file = "map.png"
            try:
                with open(map_file, "wb") as file:
                    file.write(response.content)
            except IOError as ex:
                print("Ошибка записи временного файла:", ex)
                sys.exit(2)

            # Инициализируем pygame
            pygame.init()
            screen = pygame.display.set_mode((600, 450))
            # Рисуем картинку, загружаемую из только что созданного файла.
            screen.blit(pygame.image.load(map_file), (0, 0))
            # Переключаем экран и ждем закрытия окна.
            pygame.display.flip()
            while pygame.event.wait().type != pygame.QUIT:
                pass
            pygame.quit()

            # Удаляем за собой файл с изображением.
            os.remove(map_file)

        else:
            print("Ошибка выполнения запроса:")
            print(map_api_server, params=map_params)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
    except:
        print("Запрос не удалось выполнить. Проверьте подключение к сети Интернет.")
        sys.exit(1)


def get_coordinate(address):
    from geocode import geocode
    """ координаты объекта по его адресу
    обращаемся к функции geocode из файла geocode.py"""
    toponym = geocode(address)
    if toponym:
        return toponym["Point"]["pos"]
    return None



def main():
    toponym = " ".join(sys.argv[1:])

    if toponym:
        # Показываем карту с фиксированным масштабом.
        show_map(get_coordinate(toponym), delta='15', map_type='map')

        # Показываем карту с масштабом, подобранным по заданному объекту.
        show_map(get_coordinate(toponym), str(bolder(toponym)), map_type='map')

        # Добавляем исходную точку на карту.
        show_map(get_coordinate(toponym), str(bolder(toponym)), map_type='map', pt=True)
    else:
        print('Нет парамметров')


if __name__ == "__main__":
    main()