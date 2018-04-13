from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import finger
import json
import db

app = Flask(__name__)
fing = finger._Finger()

curr_id = None

@app.route('/')
def hello():
    return render_template('index.html',running=fing.isrunning())

@app.route('/add',methods=['GET'])
def add():
    return render_template('add.html')

@app.route('/add',methods=['POST'])
def addfinger():
    name = request.form['name']
    num = request.form['num']
    data = None
    if(fing.isrunning()):
        data = {
            "status":False,
            "error":"device is running"
        }
        return json.dumps(data)
    if(int(num) == 1):
        curr_id = db.adduser(name)
    status = fing.addfinger(num,curr_id,1)
    if status == finger.SUCCESS:
        data = {
            "status":True
        }
    else:
        data = {
            "status":False,
            "error":finger.ACK_ERROR[status]
        }
    return json.dumps(data)

@app.route("/manager",methods=['GET'])
def manager():
    users = db.getusers()
    return render_template("manager.html",users=users)

@app.route("/del/<id>",methods=['GET'])
def delete(id):
    db.delteuser(id)
    return redirect(url_for('manager'))