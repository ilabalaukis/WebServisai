from flask import Flask
from redis import Redis
from flask import jsonify
from flask import request
from flask import abort

import os

app = Flask(__name__)

albums = [
			{'ID' : '1', 'Album' : 'Brain Eno', 'Artist' : 'Reflection', 'Genre' : 'Ambient', 'Producer' : 'Brian Eno'},
			{'ID' : '2', 'Album' : 'Chief Keef', 'Artist' : 'Two Zero One Seven', 'Genre' : 'Drill', 'Producer' : 'Chief Keef, Leek-e-Leek, Lex Luger, Young Chop'}
		]

songs = [
        	{'AlbumID' : '1', 'SongTitle' : 'Test test', 'SongID':'00001'}
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


@app.route('/albums/<albumID>', methods=['GET'])
def getSongsList(albumID):
        song_choose = [song for song in albums if song['ID'] == albumID]
        if len(song_choose) == 0:
                abort(404)
        return jsonify({'songs': song_choose[0]})

@app.route('/albums/<albumID>', methods=['PUT'])
def updateAlbums(albumID):
        update_album = [album for album in albums if album['ID'] == albumID]
        if len(update_album) == 0:
                abort(404)
        if not request.json:
                abort(400)
        if 'Album' in request.json and type(request.json['Album']) != unicode:
                abort(400)
        if 'Artist' in request.json and type(request.json['Artist']) != unicode:
                abort(400)
        if 'Genre' in request.json and type(request.json['Genre']) != unicode:
                abort(400)
        if 'Producer' in request.json and type(request.json['Producer']) != unicode:
                abort(400)
        update_album[0]['Album'] = request.json.get('Album', update_album[0]['Album'])
        update_album[0]['Artist'] = request.json.get('Artist', update_album[0]['Artist'])
        update_album[0]['Genre'] = request.json.get('Genre', update_album[0]['Genre'])
        update_album[0]['Producer'] = request.json.get('Producer', update_album[0]['Producer'])
        return jsonify({'Album': update_album[0]})

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)

	
