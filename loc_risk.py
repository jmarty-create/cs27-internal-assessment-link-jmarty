import requests

#link here currently pointing to your local test file but will point to eaws server
API_URL = "http://127.0.0.1:5000/static/sample_bulletin.json"


def get_eaws_danger_level(location):
    if not location:
        return None

    user_loc = location.strip().lower()
    #request data from api with 10 second saftey limit
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        #convert raw file into a python dictionary
        data = response.json()
        #loop through avalanche report
        for bulletin in data.get("bulletins",[]):
            #fomrat region to match
            regions = [str(r).lower().strip() for r in bulletin.get("regions", [])]
            if user_loc in regions:
                #check if loc exists and extract and voncert danger rating to str
                ratings = bulletin.get("dangerRatings", [])
                if ratings:
                    danger = int(ratings[0]["mainValue"])
                    if 1<=danger <=5:
                        return danger
    except (requests.RequestException,ValueError,KeyError,TypeError,AttributeError):
        return None