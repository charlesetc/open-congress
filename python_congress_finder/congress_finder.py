from geopy import geocoders
from bs4 import BeautifulSoup
import random, sys, json, urllib

gmaps = geocoders.GoogleV3()

API_KEY = 'in_office=true&apikey=55bfc2ea51944ba58364c6f1d84103d1'

com_baseURL = 'http://congress.api.sunlightfoundation.com/committees?'
leg_baseURL = 'http://congress.api.sunlightfoundation.com/legislators?'
loc_baseURL = 'http://congress.api.sunlightfoundation.com/placeholder/locate?'

govtrack_baseURL = 'https://www.govtrack.us/congress/members/'

all_states = ''' Alabama, Alaska, Arizona, Arkansas, California, Colorado, Connecticut, Delaware, District Of Columbia,
Florida, Georgia, Hawaii, Idaho, Illinois, Indiana, Iowa, Kansas, Kentucky, Louisiana, Maine, Maryland, Massachusetts,
Michigan, Minnesota, Mississippi, Missouri, Montana, Nebraska, Nevada, New Hampshire, New Jersey, New Mexico, New York,
North Carolina, North Dakota, Ohio, Oklahoma, Oregon, Pennsylvania, Rhode Island, South Carolina,
South Dakota, Tennessee, Texas, Utah, Vermont, Virginia, Washington, West Virginia, Wisconsin, Wyoming'''.split(',')


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

# gets a random congressman
def getRandomAny():
    state_name = '%20'.join(random.choice(all_states).split())
    return random.choice(json.load(urllib.urlopen(leg_baseURL + 'state_name=' + state_name + '&' + API_KEY))['results'])

# gets a random representative in the house
def getRandomInHouse():
    chamber = '&chamber=house'
    state_name = '%20'.join(random.choice(all_states).split())
    return random.choice(json.load(urllib.urlopen(leg_baseURL + 'state_name=' + state_name + chamber + '&' + API_KEY))['results'])

# gets a random senator
def getRandomInSenate():
    chamber = '&chamber=senate'
    state_name = '%20'.join(random.choice(all_states).split())
    return random.choice(json.load(urllib.urlopen(leg_baseURL + 'state_name=' + state_name + chamber + '&' + API_KEY))['results'])

# gets the image of a congressman or senator by their ID
def getImageByID(bio_guideID):
    #soup = BeautifulSoup()
    curOfficial = getRepByID(bio_guideID)['results'][0]
    soup = BeautifulSoup(urllib.urlopen(govtrack_baseURL + str(curOfficial['govtrack_id'])))
    return {'image' : 'https://www.govtrack.us' + soup.find('img', attrs = {'class': 'img-responsive'}).get('src')}



# calls a function earlier in the program
def main():
    if len(sys.argv) > 1:
        funcs = {
            'getRepsByAddress' : getRepsByAddress,
            'getRepByName' : getRepByName,
            'getRepByID' : getRepByID,
            'getDistrict' : getDistrict,
            'getAllReps' : getAllReps,
            'getCommitteeByID' : getCommitteeByID,
            'getRandomAny' : getRandomAny,
            'getRandomInHouse':getRandomInHouse,
            'getRandomInSenate': getRandomInSenate,
            'getImageByID' : getImageByID
        }

        print(json.dumps(funcs[sys.argv[1]](*sys.argv[2:])))
        return

    print("Ran without parameters")

if __name__ == "__main__":
    main()
