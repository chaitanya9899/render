from flask import Flask, render_template, request
from model import train_svm, test_svm, predict_svm
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import csv
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from time import time
from flask import *
import joblib

app = Flask(__name__)

@app.route("/")
def main():
    # return the homepage
    return render_template("login.html")

@app.route("/register")
def register():
    # return the homepage
    return render_template("register.html")

@app.route("/login")
def login():
    # return the homepage
    return render_template("login.html")

@app.route("/home")
def home():
    # return the homepage
    return render_template("index.html")

@app.route("/signup")
def signup():
    name = request.args.get('username','')
    dob = request.args.get('DOB','')
    sex = request.args.get('Sex','')
    contactno = request.args.get('CN','')
    email = request.args.get('email','')
    martial = request.args.get('martial','')
    password = request.args.get('psw','')

    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("insert into `accounts` (`name`, `dob`,`sex`,`contact`,`email`,`martial`, `password`) VALUES (?, ?, ?, ?, ?, ?, ?)",(name,dob,sex,contactno,email,martial,password))
    con.commit()
    con.close()

    return render_template("login.html")

@app.route("/signin")
def signin():
    mail1 = request.args.get('uname','')
    password1 = request.args.get('psw','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("select `email`, `password` from accounts where `email` = ? AND `password` = ?",(mail1,password1,))
    data = cur.fetchone()

    if data == None:
        return render_template("login.html")

    elif mail1 == data[0] and password1 == data[1]:
        return render_template("index.html")

    
    else:
        return render_template("login.html")

@app.route('/index')
def index():
	return render_template('index.html')

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/data")
def data():
    return render_template("data.html")


@app.route('/predict', methods=['POST']) 
def predict():

	if(request.form['space']=='None'):
		data = []
		string = 'value'
		for i in range(1,31):
			data.append(float(request.form['value'+str(i)]))

		for i in range(30):
			print(data[i])

	else:
		string = request.form['space']
		data = string.split()
		print(data)
		print("Type:", type(data))
		print("Length:", len(data))
		for i in range(30):
			print(data[i])
		data = [float(x.strip()) for x in data]

		for i in range(30):
			print(data[i])

	data_np = np.asarray(data, dtype = float)
	data_np = data_np.reshape(1,-1)
	out, acc, t = predict_svm(clf, data_np)

	if(out==1):
		output = 'Malignant'
	else:
		output = 'Benign'

	acc_x = acc[0][0]
	acc_y = acc[0][1]
	if(acc_x>acc_y):
		acc = acc_x
	else:
		acc=acc_y
	return render_template('result.html', output=output, accuracy=round(acc*100,3), time=t)


	

if __name__=='__main__':
	global clf 
	clf = train_svm()
	test_svm(clf)
	app.run(debug = True)

