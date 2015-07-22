from geopy import geocoders
from bs4 import BeautifulSoup
import os, random, sys, json, urllib

gmaps = geocoders.GoogleV3()

API_KEY = 'in_office=true&apikey=55bfc2ea51944ba58364c6f1d84103d1'

com_baseURL = 'http://congress.api.sunlightfoundation.com/committees?'
leg_baseURL = 'http://congress.api.sunlightfoundation.com/legislators?'
loc_baseURL = 'http://congress.api.sunlightfoundation.com/placeholder/locate?'

govtrack_baseURL = 'https://www.govtrack.us/congress/members/'

all_states = '''Alabama, Alaska, Arizona, Arkansas, California, Colorado, Connecticut, Delaware, District Of Columbia,
Florida, Georgia, Hawaii, Idaho, Illinois, Indiana, Iowa, Kansas, Kentucky, Louisiana, Maine, Maryland, Massachusetts,
Michigan, Minnesota, Mississippi, Missouri, Montana, Nebraska, Nevada, New Hampshire, New Jersey, New Mexico, New York,
North Carolina, North Dakota, Ohio, Oklahoma, Oregon, Pennsylvania, Rhode Island, South Carolina,
South Dakota, Tennessee, Texas, Utah, Vermont, Virginia, Washington, West Virginia, Wisconsin, Wyoming'''.split(',')

basic_questions = json.loads(open(os.path.join(os.path.dirname(__file__), 'basic_questions.json'), 'r').read())

# returns all the congressmen who represent and area given a latitude and longitude
def get_data_by_loc(lat, long, data_type):
    coords = 'latitude='+str(lat)+'&'+'longitude=' + str(long)+'&'
    return json.load(urllib.urlopen(loc_baseURL.replace('placeholder', data_type) + coords + API_KEY))

# returns all representatives who represent a certain area based on address
def getRepsByAddress(address):
    coords = list(gmaps.geocode(address)[1])
    rep_results = get_data_by_loc(coords[0], coords[1], 'legislators')
    return rep_results

# returns congressman based on name
def getRepByName(first_name, last_name):
    rep_str = 'first_name=FNAME&last_name=LNAME&in_office=true&'.replace('FNAME', first_name).replace('LNAME', last_name)
    return json.load(urllib.urlopen(leg_baseURL + rep_str + API_KEY))

# returns congressman based on bio_guideID
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
    try:
        return random.choice(json.load(urllib.urlopen(leg_baseURL + 'state_name=' + state_name + '&' + API_KEY))['results'])
    except:
        return getRandomAny()

# gets a random representative in the house
def getRandomInHouse():
    chamber = '&chamber=house'
    state_name = '%20'.join(random.choice(all_states).split())
    try:
        return random.choice(json.load(urllib.urlopen(leg_baseURL + 'state_name=' + state_name + chamber + '&' + API_KEY))['results'])
    except:
        return getRandomInHouse()

# gets a random senator
def getRandomInSenate():
    chamber = '&chamber=senate'
    state_name = '%20'.join(random.choice(all_states).split())
    try:
        return random.choice(json.load(urllib.urlopen(leg_baseURL + 'state_name=' + state_name + chamber + '&' + API_KEY))['results'])
    except:
        return getRandomInSenate()

# gets the image of a congressman or senator by their ID
def getImageByID(bio_guideID):
    #soup = BeautifulSoup()
    curOfficial = getRepByID(bio_guideID)['results'][0]
    soup = BeautifulSoup(urllib.urlopen(govtrack_baseURL + str(curOfficial['govtrack_id'])))
    return {'image' : 'https://www.govtrack.us' + soup.find('img', attrs = {'class': 'img-responsive'}).get('src')}

#filters a dictionary
def filterChamberByElement(in_list, key):
    out_list = []
    for i in range(0, len(in_list)):
        if(in_list[i].get('chamber') == key):
            out_list.append(in_list[i])
    return out_list

# gets a question session, first result is correct by convention
def getBasicQuestion(address):
    acc = 0
    curFunc = None
    correct_answer = None

    question = random.choice(basic_questions)

    if(question['type'] == 'house'):
        correct_answer = random.choice(filterChamberByElement(getRepsByAddress(address)['results'], 'house'))
        curFunc = getRandomInHouse
    elif(question['type'] == 'senate'):
        correct_answer = random.choice(filterChamberByElement(getRepsByAddress(address)['results'], 'senate'))
        curFunc = getRandomInSenate
    else:
        correct_answer = random.choice(getRepsByAddress(address)['results'])
        curFunc = getRandomAny

    options = [correct_answer] #By convention the correct answer is always first in the list when returned from the api

    for i in range(0, int(question['num']) - 1): # removes duplicates
        options.append(curFunc())

    out_list = []

    for i in range(0, len(options)):
        tmp_dict = {}
        tmp_dict = {
            'first_name' : options[i].get('first_name'),
            'last_name' : options[i].get('last_name'),
            'chamber' : options[i].get('chamber'),
            'id' : options[i].get('bioguide_id')
        }
        tmp_dict['image'] = 'https://www.govtrack.us/data/photos/' + options[i].get('govtrack_id') + '-200px.jpeg'
        out_list.append(tmp_dict)

    choice_list = []

    if question['answer_type'] == 'number':
        acc = 0
        for i in range(0, len(out_list)):
            if(out_list[i].get('chamber') == question['chamber']):
                acc += 1
        tmplist = list(set(random.sample(range(0, 5), 5)))
        try:
            tmplist.remove(acc)
        except:
            pass
        random.shuffle(tmplist)
        choice_list = [acc] + tmplist
    else:
        for i in range(0, len(out_list)):
            choice_list.append(out_list[i].get('first_name') + ', ' + out_list[i].get('last_name'))

    return {
        'type' : 'basic',
        'answer_type' : question['answer_type'],
        'choice_list' : choice_list,
        'question_name': question['name'],
        'options' : out_list
    }


# calls a function earlier in the program
# passes to MEAN application for rendering and display to the user
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
            'getImageByID' : getImageByID,
            'getBasicQuestion' : getBasicQuestion
        }

        print(json.dumps(funcs[sys.argv[1]](*sys.argv[2:])))
        return

    print("Ran without parameters")

if __name__ == "__main__":
    main()
