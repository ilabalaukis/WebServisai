from flask import Flask
from redis import Redis
from flask import jsonify
from flask import request

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

@app.route('/albums/<albumID>', methods=['DELETE'])
def delete_album(albumID):
	deleted_album=[album for album in albums if (album['ID'] == albumID)]
	if len(deleted_album) == 0:
		abort(404)
	albums.remove(deleted_album[0])
	return jsonify({'Deleted album:': deleted_album[0]})

@app.route('/albums', methods=['POST'])
def new_album():
	new_alb={
		'ID' : request.json['ID'],
		'Album' : request.json['Album'],
		'Artist' : request.json['Artist'],
		'Genre' : request.json['Genre'],
		'Producer' : request.json['Producer']
	}
	albums.append(new_alb)
	return jsonify({'Added': new_alb})

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)


