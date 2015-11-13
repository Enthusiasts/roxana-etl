__author__ = 'someone'

'''
Модели данных к которым приводит transform
'''


class Entertainment(object):
    # Вот такие штуки нелоьзя проще делать?
    def __init__(self, id, title, cost, zone_title, longitude, latitude):
        self.id = id
        self.title = title
        self.cost = cost
        self.zone_title = zone_title
        self.longitude = longitude
        self.latitude = latitude


class CheckIn(object):
    def __init__(self, client_id, entertainment_id, time_id, url, time, longtitude, latitude):
        self.client_id = client_id
        self.entertainment_id = entertainment_id
        self.time_id = time_id
        self.url = url
        self.time = time
        self.longtitude = longtitude
        self.latitude = latitude


class Time(object):
    def __init__(self, id, year, month, day, day_of_week):
        self.id = id
        self.year = year
        self.month = month
        self.day = day
        self.day_of_week = day_of_week


class Client(object):
    def __init__(self, id, title, url):
        self.id = id
        self.title = title
        self.url = url


class Zone(object):
    def __init__(self, title, date_created, polygon):
        self.title = title
        self.date_created = date_created
        self.polygon = polygon
