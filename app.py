from flask import Flask, render_template, request,session,redirect
from evaluation import calculate_risk
from database import save_assessment,get_all_user_evaluations,get_single_evaluation,create_user,verify_user
from loc_risk import get_eaws_danger_level

app = Flask(__name__)
app.secret_key = "slopeguard_secret_key_123" #this is what allows me to use the "session" part in flask and helps me manage the log ins
@app.route('/')
def home():
    #telling flask to look inside templates folder, find home.html,and display it
    return render_template('home.html')

@app.route('/evaluate')
def evaluate():
    # This bit prevents the user from creating an evaluation without being logged in which helps database
    if 'user_id' not in session:
        return redirect('/login')
    #Get the real logged-in user's ID from session
    user_id = session['user_id']
    return render_template('evaluate.html')

@app.route('/calculate', methods=["POST"])
def calculate():
    eaws_mode = request.form.get("eaws_mode", "auto")
    manual_value = request.form.get("manual_eaws")
    location = request.form.get("location")
    user_id = session.get('user_id')
    # User selects manual mode
    if eaws_mode == "manual":
        if manual_value in ["1", "2", "3", "4", "5"]:
            eaws_danger = int(manual_value)
        else:
            return render_template('evaluate.html',error="Please select a manual danger level.",manual_required=True)
    # User selects automatic mode
    else:
        eaws_danger = get_eaws_danger_level(location)

        # If API fails, force manual input
        if eaws_danger is None:
            return render_template('evaluate.html',error="API unavailable. Please enter the danger level manually.",manual_required=True)
    # Add the validated danger level to the assessment inputs
    data = request.form.to_dict()
    data["eaws_danger"] = eaws_danger
    #calculate the risk using the validated inputs
    verdict, color, risk_score, eaws_danger, reason = calculate_risk(data)

    if risk_score == "N/A":
        numeric_score = 10.0
    else:
        numeric_score = float(risk_score)
    # Save the assessment to the database
    save_assessment(user_id=user_id, location=location,eaws_danger=eaws_danger, risk_score=numeric_score,verdict=verdict, color=color, reason=reason)
    #displaying the results
    return render_template('results.html', verdict=verdict,color=color, risk_score=risk_score, eaws_danger=eaws_danger, reason=reason)

@app.route('/compare', methods=["GET", "POST"])
def compare():
    # Make sure user is logged in first
    if 'user_id' not in session:
        return redirect('/login')
    # Get the real logged-in user's ID from session
    user_id = session['user_id']

    #taking the list of evaluations so the dropdown works
    past_evaluations = get_all_user_evaluations(user_id)
    result = None
    #If the user clicked compare(POST request)
    if request.method == "POST":
        past_id = request.form.get("past_id")

        if past_id and past_evaluations:
            #Get past assessment
            past_eval = get_single_evaluation(past_id)

            #Get the latest assessment(the last item in the list)
            latest_eval = past_evaluations[-1]
            past_score = past_eval[0]
            latest_score = latest_eval[2]
            if latest_score > past_score:
                result = f"Your last check ({latest_score}) is more dangerous than assessment number {past_id}. Take this into consideration and ski safely"
            elif latest_score < past_score:
                result = f"Your last check ({latest_score}) is less dangerous than assessment number {past_id}. Take this into consideration and ski safely"
            else:
                result = f"Your last check is equally as dangerous as assessment number {past_id}. Take this into consideration and ski safely"

    return render_template('compare.html', past_evaluations=past_evaluations, result=result)

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        #add to database
        create_user(username, password)
    return render_template('register.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        #Check user information in the user database
        user_id = verify_user(username, password)

        if user_id:
            session['user_id'] = user_id  #Save user session
            session['username'] = username #Store username to display
            return redirect('/')
        else:
            return "Invalid username or password! Please try again."
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()  #Log out the user
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)