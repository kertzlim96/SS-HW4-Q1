from flask import Flask, Response, render_template, redirect, url_for, request, session, abort
import sys
import random
import hashlib
from honeywords import *

app = Flask(__name__, template_folder='templates')

# config
app.config.update(
	DEBUG = True,
	SECRET_KEY = 'secret_xxx'
)


@app.route('/', methods=["GET", "POST"])
def home():
	if request.method == 'GET':
		return render_template('login.html')
    
	USER, INDEX, HASH = read_db() 

	username = request.form['username']
	password = request.form['password']

	if username not in USER:
		return Response('<p>Username does not exist. <a href="/">Login</a></p>')
	else:
		user_index = USER.index(username)
		#authenticate_pw(pw_hashlist,index, password)
		hashed_pw = md5_hash(password)
		index_real_password = int(INDEX[user_index]) # index among the hash for the real password, rest honeyword

		# case 1: Real password
		if hashed_pw in HASH[user_index] and HASH[user_index][index_real_password] == hashed_pw:
			return Response('<p>Login success. <a href="/">Login as another user</a></p>')
		
		# case 2: Honeyword
		elif hashed_pw in HASH[user_index] and HASH[user_index][index_real_password] != hashed_pw:
			return Response('<p>HONEYWORD, RAISE THE ALERT! BEE DOO BEE DOO!. <a href="/">Login</a></p>')
			
		# case 3: Wrong password
		else:
			return Response('<p>Login failure. <a href="/">Login</a></p>')


@app.route('/register', methods=["GET", "POST"])
def register():
	if 'random' not in session.keys():   
		session['random'] = random.randint(100, 999)

	if request.method == 'GET':
		return render_template('register.html')

	username = request.form['username']
	password = request.form['password'].encode('ascii', 'ignore')

	
    # wordlist to generate new honeywords
	wordlist = []    
	with open("10k-most-common.txt",'r') as f:
		for i in f:
			wordlist.append(i.rstrip())
	# open up database to check if username taken
	USER, INDEX, HASH = read_db()
	if username in USER:
		return Response('<p>Username taken. <a href="/register">Try again</a></p>')
	else:
		# adds new user, hash into _db.csv
		gen_and_add_new_user_db(username,password,wordlist)

	session.pop('random', None)

	return Response('<p>Valid registration. <a href="/">Login</a></p>')


@app.errorhandler(401)
def page_not_found(e):
	return Response('<p>Login failed</p>')


if __name__ == "__main__":
	app.run()
