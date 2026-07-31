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
    return render_template('evaluate.html')

@app.route('/calculate', methods=["POST"])
def calculate():
    if 'user_id' not in session:
        return redirect('/login')
    #Get the real logged-in user's ID from session
    user_id = session['user_id']
    ""
    eaws_mode = request.form.get("eaws_mode", "auto")
    manual_value = request.form.get("manual_eaws")
    location = request.form.get("location")

    eaws_danger = None
    #User selects manual mode
    if eaws_mode == "manual" and manual_value:
        if manual_value.isdigit():
            eaws_danger = int(manual_value)

        #If Auto mode selected or manual was empty do API lookup
    if eaws_danger is None:
        eaws_danger = get_eaws_danger_level(location)

        # fallback if API lookup is not working and no manual selection was made
    if eaws_danger is None:
        if manual_value and manual_value.isdigit():
            eaws_danger = int(manual_value)
        else:
            eaws_danger = 1  # Default fallback for now but will need to do somthing about later
    #here flask takes everything the user typed or selected in <form> using request.form
    verdict, color, risk_score, eaws_danger, reason = calculate_risk(request.form)
    if risk_score == "N/A": #In case one of the hard stops is hit where there is no score given
        numeric_score = 10.0
    else:
        numeric_score = float(risk_score)
        #This line takes all the assesment info from user details and html inputs and runs the saving function from the database file
    save_assessment(user_id=user_id, location=request.form["location"],eaws_danger=eaws_danger,risk_score=numeric_score,verdict=verdict,color=color,reason=reason)

    # render_template fills the html variables from the results and equates them to the python variable(left of equals is html and right is python that was calculated)
    return render_template('results.html',verdict=verdict,color=color,score=risk_score,eaws=eaws_danger,reason=reason)

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
                result = f"Your last check ({latest_score}) is more dangerous than assessment number {past_id}."
            elif latest_score < past_score:
                result = f"Your last check ({latest_score}) is less dangerous than assessment number {past_id}."
            else:
                result = f"Your last check is equally as dangerous as assessment number {past_id}."

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