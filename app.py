#!/usr/bin/env python3
from flask import Flask,request,render_template,flash,redirect,abort,session
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
app = Flask(__name__)
# First MYSQL Command After install
# CREATE DATABASE website;
# grant all privileges on website.* to 'admin'@'localhost' identified by 'password';
MYSQL_USER = 'admin'
MYSQL_PASSWORD = 'password'
MYSQL_HOST = 'localhost'
MYSQL_DB = 'website'
SECRET_KEY = 'fasgas'
app.config.from_object(__name__)
mysql = MySQL(app)
def encrypt(my_word,my_hash=None,hasher=None):
	if hasher:
		return sha256_crypt.encrypt(my_word)
	if my_hash != None:
		return sha256_crypt.verify(my_word, my_hash)
def mysql(mysql=mysql):
	c = mysql.connection
	cmd = c.cursor()
	return c ,cmd
@app.route('/',methods=['POST','GET'])
def login():
	if request.method == 'POST':
		r = request.form
		username = r['username']
		password = r['password']
		if len(username) < 30 and len(password) < 100:
			c,cmd = mysql()
			cmd.execute('SELECT username FROM users WHERE username = (%s)',(username,))
			data = cmd.fetchone()
			if data:
				cmd.execute('SELECT password FROM users WHERE username = (%s)',(username,))
				data = cmd.fetchone()
				data = data[0]
				if encrypt(my_word=password,my_hash=data):
					session['user'] = username
					return f'Welcome {session.get("user")}'
			flash('Error : username or password not True')
			return render_template('index.html')
	return render_template('index.html')
@app.route('/install',methods=['GET','POST'])
def install():
	if request.method == 'POST':
		c , cmd = mysql()
		cmd.execute('''CREATE TABLE `users` (   `id` int NOT NULL AUTO_INCREMENT,   `user_id` int DEFAULT NULL,   `username` varchar(100) NOT NULL,   `password` varchar(100) NOT NULL,   PRIMARY KEY (`id`) ) ENGINE=InnoDB DEFAULT CHARSET=utf8;''')
		c.commit()
		cmd.execute('''INSERT INTO `users` (`username`,`password`) VALUES ('admin','$5$rounds=535000$ztlowm/g2HYBXkYt$PWKRgp.k.YAfTYU7kvMQ7B6ezaYj2819yygvuEuAReA');''')
		c.commit()
		return '<script>alert("Done :)");window.location = "/"</script>'
	return render_template('install.html')
if __name__ == '__main__':
	app.run(debug=True)