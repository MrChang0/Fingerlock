from gevent import monkey
monkey.patch_all()
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import finger
import json
from gevent import pywsgi
import db

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'  
fing = finger._Finger()

def start():
    fing.start()
    server = pywsgi.WSGIServer(('0.0.0.0',5000), app)
    server.serve_forever()

@app.route('/')
def hello():
    return render_template('index.html', running=fing.isrunning())

@app.route('/index')
def index():
    return render_template('index.html', running=fing.isrunning())

@app.route('/start',methods=['GET'])
def fingstart():
    fing.start()
    return redirect(url_for('index'))

@app.route('/add', methods=['GET'])
def add():
    return render_template('add.html')


@app.route('/add', methods=['POST'])
def addfinger():
    name = request.form['name']
    num = request.form['num']
    curr_id = None
    if int(num) == 1:
        curr_id = db.adduser(name)
        session['curr_id'] = curr_id
    else:
        curr_id = session['curr_id']
    status = fing.addfinger(num, curr_id, 1)
    if status == finger.SUCCESS:
        data = {
            "status": True
        }
    else:
        data = {
            "status": False,
            "error": finger.ACK_ERROR[status]
        }
    return json.dumps(data)


@app.route("/manager", methods=['GET'])
def manager():
    users = db.getusers()
    return render_template("manager.html", users=users)


@app.route("/del/<id>", methods=['GET'])
def delete(id):
    db.delteuser(id)
    fing.delfinger(int(id))
    return redirect(url_for('manager'))
