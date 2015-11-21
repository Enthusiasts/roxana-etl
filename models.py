__author__ = 'someone'

'''
Модели данных к которым приводит transform
'''


class Entertainment(object):
    # Вот такие штуки нелоьзя проще делать?
    def __init__(self, title, cost, zone_title, longitude, latitude, seats_count, social_priveleges):
        self.title = title
        self.cost = cost
        self.zone_title = zone_title
        self.longitude = longitude
        self.latitude = latitude
        self.seats_count = seats_count
        self.social_priveleges = social_priveleges


class CheckIn(object):
    # TODO: Удалить из конструктора client_id, entertainment_id, time_id
    def __init__(self, url, datetime, longitude, latitude, username):
        self.url = url
        self.datetime = datetime  # Тип datetime!
        self.longtitude = longitude
        self.latitude = latitude
        self.username = username

        self.client_id = 0
        self.entertainment_id = 0
        self.time_id = 0


class Time(object):
    # TODO: удалить, он теперь бесполезен
    def __init__(self, year, month, day, day_of_week):
        self.year = year
        self.month = month
        self.day = day
        self.day_of_week = day_of_week


class Client(object):
    def __init__(self, title, url):
        self.title = title
        self.url = url


class Zone(object):
    def __init__(self, title, date_created, polygon):
        self.title = title
        self.date_created = date_created
        self.polygon = polygon
