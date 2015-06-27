import json, urllib
from geopy import geocoders

gmaps = geocoders.GoogleV3()

API_KEY = 'apikey=55bfc2ea51944ba58364c6f1d84103d1'
com_baseURL = 'http://congress.api.sunlightfoundation.com/committees?'
leg_baseURL = 'http://congress.api.sunlightfoundation.com/legislators?'
loc_baseURL = 'http://congress.api.sunlightfoundation.com/placeholder/locate?'

# returns all the congressmen who represent and area given a latitude and longitude
def get_data_by_loc(lat, long, data_type):
    coords = 'latitude='+str(lat)+'&'+'longitude=' + str(long)+'&'
    return json.load(urllib.urlopen(loc_baseURL.replace('placeholder', data_type) + coords + API_KEY))

# returns all representatives who represent a certain area based on address
def getRepsByAddress(address):
    coords = list(gmaps.geocode(address)[1])
    rep_results = get_data_by_loc(coords[0], coords[1], 'legislators')
    return rep_results

def getRepByName(first_name, last_name):
    rep_str = 'first_name=FNAME&last_name=LNAME&in_office=true&'.replace('FNAME', first_name).replace('LNAME', last_name)
    return json.load(urllib.urlopen(leg_baseURL + rep_str + API_KEY))

def getRepByID(bio_guideID):
    id_str = 'bioguide_id=CUR_ID&'.replace('CUR_ID', str(bio_guideID))
    return json.load(urllib.urlopen(leg_baseURL + id_str + API_KEY))

# returns the district of an address
def getDistrict(address):
    coords = list(gmaps.geocode(address)[1])
    dist_results = get_data_by_loc(coords[0], coords[1], 'districts')
    return dist_results

# gets all congressional representatives
def getAllReps():
    all_congress_call = 'http://congress.api.sunlightfoundation.com/legislators?in_office=true&apikey=55bfc2ea51944ba58364c6f1d84103d1'
    return json.load(urllib.urlopen(all_congress_call))

# gets the committees of a given congressman by ID
def getCommitteeByID(bio_guideID):
    return json.load(urllib.urlopen(com_baseURL + 'member_ids=' + str(bio_guideID) + '&' + API_KEY))

