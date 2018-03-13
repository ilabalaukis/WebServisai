from flask import Flask
from redis import Redis
from flask import jsonify

import os

app = Flask(__name__)

albums = [
			{'ID' : '1', 'Album' : 'Brain Eno', 'Artist' : 'Reflection', 'Genre' : 'Ambient', 'Producer' : 'Brian Eno'},
			{'ID' : '2', 'Album' : 'Chief Keef', 'Artist' : 'Two Zero One Seven', 'Genre' : 'Drill', 'Producer' : 'Chief Keef, Leek-e-Leek, Lex Luger, Young Chop'}
			]

redis = Redis(host='redis', port=6379)

@app.route('/')
def hello():
	return 'List of albums'

@app.route('/albums/', methods=['GET'])
def getAllInfo():
	return jsonify({'Information':albums})

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
