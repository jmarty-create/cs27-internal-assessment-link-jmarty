def fetch_eaws_danger(location):
   #Looks up regional avalanche danger level (1 to 5) normally but am using these if statements to test and palcehold for now.
   loc = location.lower().strip()
   if "thyon" in loc:
       return 5
   elif "verbier" in loc:
       return 3
   elif "champery" in loc:
       return 1

def calculate_risk(data):
    #This is the function that will evaluate the inputs and give feedback but doesnt return anything at the moment
    return None