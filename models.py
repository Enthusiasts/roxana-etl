# Enthusiasts, 2015

'''
Модели данных к которым приводит transform
'''


class CommonEqualityMixin(object):

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return str(self.__dict__)


class Entertainment(CommonEqualityMixin):
    def __init__(self, title, cost, zone_title, longitude, latitude, seats_count, social_priveleges, type, global_id):
        self.title = title
        self.cost = cost
        self.zone_title = zone_title
        self.longitude = longitude
        self.latitude = latitude
        self.seats_count = seats_count
        self.social_priveleges = social_priveleges
        self.type = type
        self.global_id = global_id

    def __eq__(self, other):
        return self.longitude == other.longitude and self.latitude == other.latitude and self.title == other.title

    def __hash__(self):
        return 961 * self.longitude.__hash__() + 31*self.latitude.__hash__() + self.title.__hash__()


class CheckIn(object):
    def __init__(self, url, datetime, longitude, latitude, username, username_url):
        self.url = url
        self.datetime = datetime  # Тип datetime!
        self.longtitude = longitude
        self.latitude = latitude
        self.username = username
        self.username_url = username_url

        self.client_id = -1
        self.entertainment_id = -1
        #self.time_id = -1

    def __eq__(self, other):
        #return self.client_id == other.client_id and self.entertainment_id == other.entertainment_id #and self.time_id == other.time_id
        return self.url == other.url

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        #return int(963*self.entertainment_id) + int(self.client_id) #+ int(31*self.time_id)
        return self.url.__hash__()


class Client(CommonEqualityMixin):
    def __init__(self, title, url):
        self.title = title
        self.url = url

    def __eq__(self, other):
        return self.title == other.title and self.url == other.url

    def __hash__(self):
        return 31*self.title.__hash__() + self.url.__hash__()


class Zone(CommonEqualityMixin):
    def __init__(self, title, date_created, polygon):
        self.title = title
        self.date_created = date_created
        self.polygon = polygon


# Самый полезный класс здесь
class Time(CommonEqualityMixin):
    def __init__(self, datetime):
        self.datetime = datetime

