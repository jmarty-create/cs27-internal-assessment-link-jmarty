from flask import Flask, render_template, request, session
from evaluation import calculate_risk
from database import save_assessment

app = Flask(__name__)
@app.route('/')
def home():
    #telling flask to look inside templates folder, find home.html,and display it
    return render_template('home.html')

@app.route('/evaluate')
def evaluate():
    return render_template('evaluate.html')


@app.route('/calculate', methods=['POST'])
def calculate():
   # here flask takes everything the user typed or selected in <form> using request.form
   verdict, color, risk_score, eaws_danger, reason = calculate_risk(request.form)
   user_id = 1 #palceholder for now because I havent implimented log in system
   if risk_score == "N/A": #In case one of the hard stops is hit where there is no score given
       numeric_score = 10.0
   else:
       numeric_score = float(risk_score)
    #This line takes all the assesment info from user details and html inputs and runs the saving function from the database file
   save_assessment(user_id=user_id, location=request.form["location"],eaws_danger=eaws_danger,risk_score=numeric_score,verdict=verdict,color=color,reason=reason)

    # render_template fills the html variables from the results and equates them to the python variable(left of equals is html and right is python that was calculated)
   return render_template('results.html',verdict=verdict,color=color,score=risk_score,eaws=eaws_danger,reason=reason)

if __name__ == '__main__':
    app.run(debug=True)