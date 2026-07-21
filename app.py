from flask import Flask, render_template, request
from evaluation import calculate_risk

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


   # render_template fills the html variables from the results and equates them to the python variable(left of equals is html and right is python that was calculated)
   return render_template('results.html',verdict=verdict,color=color,score=risk_score,eaws=eaws_danger,reason=reason)

if __name__ == '__main__':
    app.run(debug=True)