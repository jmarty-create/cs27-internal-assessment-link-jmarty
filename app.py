from flask import Flask, render_template

app = Flask(__name__)
@app.route('/Home Page')
def home():
    #telling flask to look inside templates folder, find index.html, and display it
    return render_template('home.html')
if __name__ == '__main__':
    app.run(debug=True)