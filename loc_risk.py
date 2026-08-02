import requests

#link here currently pointing to your local test file but will point to eaws server
API_URL = "http://127.0.0.1:5000/static/sample_bulletin.json"


def get_eaws_danger_level(location):
    user_loc = location.strip().lower()
    #request data from api with 10 second saftey limit
    response = requests.get(API_URL, timeout=10)
    if response.status_code == 200: #200 is http status code for data passing through correctly
        #convert raw file into a python dictionary
        data = response.json()
        #loop through avalanche report
        for bulletin in data.get("bulletins"):
            #fomrat region to match
            regions = [str(r).lower().strip() for r in bulletin.get("regions", [])]
            if user_loc in regions:
                #check if loc exists and extract and voncert danger rating to str
                ratings = bulletin.get("dangerRatings", [])
                if ratings:
                    return int(ratings[0]["mainValue"])