__author__ = 'someone'

'''
Модели данных к которым приводит transform
'''


class Entertainment(object):
    # Вот такие штуки нелоьзя проще делать?
    def __init__(self, title, cost, zone_title, longtitude, latitude):
        self.title = title
        self.cost = cost
        self.zone_title = zone_title
        self.longtitude = longtitude
        self.latitude = latitude


class CheckIn(object):
    def __init__(self):
        pass


class Time(object):
    def __init__(self):
        pass


class Client(object):
    def __init__(self):
        pass


class Zone(object):
    def __init__(self):
        pass
