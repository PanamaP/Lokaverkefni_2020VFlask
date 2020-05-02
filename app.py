import pyrebase
from flask import Flask, render_template, request, redirect, url_for, session
from config import *
import os

app = Flask(__name__)
app.secret_key = os.urandom(8)

config = {
    "apiKey": api_key,
    "authDomain": "lokaverkefni-9d19d.firebaseapp.com",
    "databaseURL": "https://lokaverkefni-9d19d.firebaseio.com",
    "projectId": "lokaverkefni-9d19d",
    "storageBucket": "lokaverkefni-9d19d.appspot.com",
    "messagingSenderId": "430689612910",
    "appId": "1:430689612910:web:8ba12485d49f86865be27f",
    "measurementId": "G-SJ7E9MRD03"
}

fb = pyrebase.initialize_app(config)
db = fb.database()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/innskra')
def login():
    return render_template("innskra.html")


@app.route('/login', methods=['GET', 'POST'])
def dologin():
    login = False
    if request.method == 'POST':

        user = request.form['user']
        pwd = request.form['psw']

        u = db.child('user').get().val()
        lst = list(u.items())
        for i in lst:
            if user == i[1]['user'] and pwd == i[1]['pwd']:
                login = True
                break

        if login:
            session['logged_in'] = user
            return redirect("/bifreidaskra")
        else:
            return render_template("nologin.html")
    else:
        return render_template("no_method.html")


@app.route('/nyskra')
def nyskra():
    return render_template("nyskra.html")


@app.route('/adnyskra', methods=['GET', 'POST'])
def doregister():
    usernames = []
    if request.method == 'POST':

        user = request.form['user']
        pwd = request.form['psw']

        u = db.child('user').get().val()
        lst = list(u.items())
        for i in lst:
            usernames.append(i[1]['user'])

        if user not in usernames:
            db.child('user').push({"user": user, "pwd": pwd})
            return render_template("nyskradur.html")
        else:
            return render_template("notanditil.html")
    else:
        render_template("no_method.html")


@app.route('/bifreidaskra')
def bifreidaskra():
    if 'logged_in' in session:
        u = db.child("bill").get().val()
        lst = list(u.items())
        return render_template("bifreidaskra.html", bilar=lst)
    else:
        return redirect("/utskra")


@app.route('/bill/<id>')
def bill(id):
    u = db.child('bill').child(id).get().val()
    lst = list(u.items())
    return render_template('bill.html', bill=lst, id=id)


@app.route('/nyskrabil')
def nyskrabil():
    return render_template("nyskrabil.html")


@app.route('/donyskrabil', methods=['GET', 'POST'])
def donyskrabil():
    bill = []
    if request.method == 'POST':

        nr = request.form['nr']
        tegund = request.form['tegund']
        utegund = request.form['utegund']
        argerd = request.form['argerd']
        akstur = request.form['akstur']

        u = db.child('bill').get().val()
        lst = list(u.items())
        for i in lst:
            bill.append(i[1]['nr'])

        if nr not in bill:
            db.child('bill').push({"nr": nr, "tegund": tegund, "utegund": utegund, "argerd": argerd, "akstur": akstur})
            return render_template("nyskradurbill.html", nr=nr)
        else:
            return render_template("bilnrtil.html")
    else:
        render_template("no_method.html")


@app.route('/breytaeyda', methods=['POST'])
def breytaeyda():
    if request.method == 'POST':
        if request.form['submit'] == 'eyda':
            db.child("bill").child(request.form['id']).remove()
            return render_template('eytt.html', nr=request.form['nr'])
        else:
            db.child("bill").child(request.form['id']).update({"nr": request.form['nr'],
                                                               "tegund": request.form['tegund'],
                                                               "utegund": request.form['utegund'],
                                                               "argerd": request.form['argerd'],
                                                               "akstur": request.form['akstur']})
            return render_template('uppfaert.html', nr=request.form['nr'])
    else:
        return render_template("no_method.html")


@app.route('/utskra')
def logout():
    session.pop("logged_in", None)
    return render_template("utskra.html")


if __name__ == "__main__":
    app.run(debug=True)
