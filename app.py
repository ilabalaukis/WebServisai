from flask import Flask
from redis import Redis
from flask import jsonify

import os

app = Flask(__name__)

albums = [
			{'ID' : '1', 'Album' : '', 'Artist' : '', 'Genre' : '', 'Producer' : ''},
			{'ID' : '1', 'Album' : '', 'Artist' : '', 'Genre' : '', 'Producer' : ''}
			]

redis = Redis(host='redis', port=6379)

@app.route('/')
def hello():
	return 'List of albums'

@app.route('/albums', methods=['GET'])
def getAllInfo():
	return jsonify({'Information':albums})

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)