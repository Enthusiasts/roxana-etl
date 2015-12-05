# Enthusiasts, 2015

'''
Модели данных к которым приводит transform
'''


class Entertainment(object):
    def __init__(self, title, cost, zone_title, longitude, latitude, seats_count, social_priveleges, type):
        self.title = title
        self.cost = cost
        self.zone_title = zone_title
        self.longitude = longitude
        self.latitude = latitude
        self.seats_count = seats_count
        self.social_priveleges = social_priveleges
        self.type = type


class CheckIn(object):
    def __init__(self, url, datetime, longitude, latitude, username, username_url):
        self.url = url
        self.datetime = datetime  # Тип datetime!
        self.longtitude = longitude
        self.latitude = latitude
        self.username = username
        self.username_url = username_url

        self.client_id = None
        self.entertainment_id = None
        self.time_id = None


class Client(object):
    def __init__(self, title, url):
        self.title = title
        self.url = url


class Zone(object):
    def __init__(self, title, date_created, polygon):
        self.title = title
        self.date_created = date_created
        self.polygon = polygon


# Самый полезный класс здесь
class Time(object):
    def __init__(self, datetime):
        self.datetime = datetime
