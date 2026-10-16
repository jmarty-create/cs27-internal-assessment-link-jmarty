from loc_risk import get_eaws_danger_level
def calculate_risk(data):
    #take out inputs on sections that the user fills in
    location = data["location"]
    angle = int(data["slope_angle"])
    aspect = data["slope_aspect"]
    familiarity = data["familiarity"]
    group_size = data["group_size"]

    #assume intially all checkboxes are unchecke
    #(am using these variables because is more organized than using data.get("gear") in rest of code)
    has_transceiver = False
    has_probe = False
    has_shovel = False
    has_airbag = False
    # update to true if is ticked to "yes"
    if data.get("gear_transceiver") == "yes":
        has_transceiver = True
    if data.get("gear_probe") == "yes":
        has_probe = True
    if data.get("gear_shovel") == "yes":
        has_shovel = True
    if data.get("gear_airbag") == "yes":
        has_airbag = True

    #avalanche danger has already been checked in app.py
    eaws_danger = int(data["eaws_danger"])

    # the automatic hard stops that lead to immediate "No-go"
    if has_transceiver == False:
        return "No-Go", "red", "N/A", eaws_danger, "Automatic No-Go: Missing Transceiver!"
    elif group_size == "1":
        return "No-Go", "red", "N/A", eaws_danger, "Automatic No-Go: Solo skiing is not allowed."
    elif eaws_danger >= 4:
        return "No-Go", "red", "N/A", eaws_danger, "Automatic No-Go: EAWS Danger Level Extreme."

    # Calculating natural factors (50% of overall score)
    if 35 <= angle <= 40:
        angle_score = 10.0  #Highest number of avalanches
    elif (30 <= angle < 35) or (41 <= angle <= 45):
        angle_score = 8.0  # High risk avalanche terrain
    elif angle > 45:
        angle_score = 5.0  # Very steep but snow doesn't pile up as much to cause avalanches
    else:
        angle_score = 2.0  # Less steep area so lower risk
    if aspect == "N" or aspect =="NE" or aspect == "E" or aspect == "NW":
        aspect_score = 8.0  # Areas in the shade are colder lead to higher risk of avalanches(Northern Hemisphere)
    else:
        aspect_score = 3.0
    # Combine natural variables and scale to 50% weighting
    natural_raw_average = (angle_score + aspect_score + (eaws_danger * 2)) / 3.0
    natural_component = natural_raw_average * 0.50

    #Gear factors (25% of overall score)
    # Start at maximum gear risk (10) and subtract points for each item
    gear_risk = 10.0
    if has_shovel:
        gear_risk -= 2.5
    if has_probe:
        gear_risk -= 2.5
    if has_airbag:
        gear_risk -= 2.0
    # Subtract for transceiver (guaranteed present due to hard-stop check above)
    gear_risk -= 3.0
    gear_component = gear_risk * 0.25

    # Group/human factors (25% of overall score)
    if group_size == "3-4":
        human_score = 2.0  # Optimal group size
    elif group_size == "2":
        human_score = 4.0
    else:
        human_score = 7.0  # 5+ group size is too much pressure on snow

    #Adjust human risk based on terrain familiarity
    if familiarity == "first_time":
        human_score += 2.0
    elif familiarity == "sometimes":
        human_score += 1.0

    human_component = human_score * 0.25

    #Combine everything together
    total_risk = natural_component + gear_component + human_component

    if total_risk >= 7.0:
        verdict = "No-Go"
        color = "red"
        reason = "Combined natural, gear, and group risk score is too high."
    elif total_risk >= 4.0:
        verdict = "Medium Risk"
        color = "orange"
        reason = "Exercise heightened caution and assess local snowpack carefully."
    else:
        verdict = "Low Risk"
        color = "green"
        reason = "Conditions and group preparations are within favorable safety parameters."
    return verdict, color, round(total_risk,2), eaws_danger, reason