import requests
from datetime import datetime
import re
from random import randint
from transliterate import slugify


def loadauthdata():
    authfile = open('AuthDataFile', 'r')
    clientid = authfile.readline()
    secret = authfile.readline()
    authfile.close()
    authdata = {'client_id': clientid, 'client_secret': secret, 'v': datetime.now().strftime('%Y%m%d')}
    return authdata


def getcategoryreq(authdata):
    categoryReq = requests.get('https://api.foursquare.com/v2/venues/categories', params=authdata)
    return categoryReq.json()


def getplaceid(location, name, authdata):
    authdata['ll']=location
    findrequest = requests.get('https://api.foursquare.com/v2/venues/search', params=authdata)
    venues = findrequest.json()["response"]["venues"]
    temp = textprepairer(name)
    for dict in venues:
        n = dict.get('name').lower()
        if (temp[0] in n) or (temp[1] in n):
            return dict.get('id')


def getvenueinfo(placeid, authdata):
    try:
        venueinforeq = requests.get('https://api.foursquare.com/v2/venues/'+placeid+'/', params=authdata)
        info = venueinforeq.json()["response"]["venue"] #now do with it just what u want
        return (info["price"]).get('tier')
    except:
        return randint(1,3)


def textprepairer(text): #func that prepare text from db to format we need
    if '«' in text:
        temp = re.search(r'«(.*)»', text)
        a = temp.group(1)
        return [a.lower(), (slugify(a).lower()).replace('-', ' ')]
    else:
        return [text.lower(), ((slugify(text)).lower()).replace('-', ' ')]


# TODO: Remove
# temp = getplaceid('55.857319,37.432131', 'Corneli Pizza', loadauthdata())
# print(getvenueinfo(temp, loadauthdata()))


def __get_cost(lon, lat, name, auth_data):
    lon1= "%10.3f"%lon
    lat1="%10.3f"%lat
    ll = lon1 + ',' + lat1
    ll = ll.replace(' ', '')
    return getvenueinfo(getplaceid(ll, name, auth_data), auth_data)


def get_cost_info(lon, lat, name):
    a_data = loadauthdata()
    return __get_cost(lon, lat, name, a_data)


def get_costs_info(data):  # data is list of (lon, lan name) tuples
    a_data = loadauthdata()
    return map(lambda dat: __get_cost(dat[0], dat[1], dat[2], a_data), data)

