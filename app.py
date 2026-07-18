from flask import Flask, render_template

app = Flask(__name__)
@app.route('/')
def home():
    #telling flask to look inside templates folder, find home.html, and display it
    return render_template('home.html')
if __name__ == '__main__':
    app.run(debug=True)