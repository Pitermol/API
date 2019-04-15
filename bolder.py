import requests
from geocode import geocode

def bolder(address):
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
