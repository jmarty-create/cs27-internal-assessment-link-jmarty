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
    #take out inputs on sections that the user fills in
    location = data["location"]
    angle = int(data["slope_angle"])
    aspect = data["slope_aspect"]
    familiarity = data["famliiarity"]
    group_size = data["group_size"]

    #assume intially all checkboxes are unchecke
    #(am using these variables because is more organized than using data.get("gear") in rest of code)
    has_transceiver = False
    has_probe = False
    has_shovel = False
    has_airbag = False

    # update to True if is ticked to "yes"
    if data.get("gear_transceiver") == "yes":
        has_transceiver = True
    if data.get("gear_probe") == "yes":
        has_probe = True
    if data.get("gear_shovel") == "yes":
        has_shovel = True
    if data.get("gear_airbag") == "yes":
        has_airbag = True

    # avalanche danger from function above
    eaws_danger = fetch_eaws_danger(location)

    #the automatic hard stops that lead to immediate "No-go"
    if has_transceiver == False:
        return "No-Go", "red", "N/A", eaws_danger, "Automatic No-Go: Missing Transceiver!"
    elif group_size == "1":
        return "No-Go", "red", "N/A", eaws_danger, "Automatic No-Go: Solo skiing is not allowed."
    elif eaws_danger == 5:
        return "No-Go", "red", "N/A", eaws_danger, "Automatic No-Go: EAWS Danger Level 5(Extreme)."
