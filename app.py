# -*- encoding: utf-8 -*-

from flask import Flask
from MyClass import Server
import sys


app = Flask(__name__)
port = 8081
app.debug = True
s = Server(sys.path[0]) #传递当前目录

@app.route('/')
def hello():
	return s.index()

@app.route('/get/<filename>', methods=['GET', 'POST'])
def send(filename):
	return app.send_static_file(filename)

@app.route('/list')
def list():
	return s.list()

@app.route('/go', methods = ['POST'])
def go():
	return s.go()

@app.route('/play/<filename>')
def play(filename):
	return s.play(filename)

if __name__ == '__main__':
	app.run(port=port)
