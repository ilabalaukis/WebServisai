from flask import Flask
from flask import jsonify
from flask import request
from flask import abort
from flask_spyne import Spyne
from spyne.protocol.soap import Soap11
from spyne.model.primitive import Unicode, Integer
from spyne.model.complex import Iterable, Array, ComplexModel
import json
import requests
import os

app = Flask(__name__)
spyne = Spyne(app)
albums = [
        {
        'ID' : '1',
        'Album' : 'Brain Eno',
        'Artist' : 'Reflection',
        'Genre' : 'Jazz',
        'Producer' : 'Brian Eno',
        'MovieID' : '3'
        },
        {
         'ID' : '2',
         'Album' : 'Chief Keef', 
         'Artist' : 'Two Zero One Seven', 
         'Genre' : 'Jazz', 
         'Producer' : 'Chief Keef, Leek-e-Leek, Lex Luger, Young Chop',
         'MovieID' : '2'
         }
]

@app.route('/')
def hello():
    return 'List of albums'

@app.route('/movies', methods=['GET'])
def getMovies():
    r = requests.get('http://web2:81/movies').text
    r = json.loads(r)
    return jsonify(r), 200
    
#@app.route('/albums', methods=['GET'])
#def getAllInfo():
#   return jsonify(albums)

@app.route('/albums/genre/<genre>', methods=['GET'])
def getGenreList(genre):
        genre_choose = [genreName for genreName in albums if genreName['Genre'] == genre]
        if len(genre_choose) == 0:
                abort(404)
        return jsonify(genre_choose)

#@app.route('/albums/<albumID>', methods=['GET'])
#def getAlbum(albumID):
#        album_choose = [album for album in albums if album['ID'] == albumID]
#        if len(album_choose) == 0:
#                abort(404)
#        album_choose = jsonify(album_choose)
#        return album_choose 

@app.route('/albums/<albumID>', methods=['DELETE'])
def delete_album(albumID):
    deleted_album = [album for album in albums if (album['ID'] == albumID)]
    if len(deleted_album) == 0:
        abort(404)
    albums.remove(deleted_album[0])
    return albumID

@app.route('/albums', methods=['POST'])
def new_album_movie():
    if(request.args.get('embedded', '') == "movie"):
        album = request.json['MovieID']
        url = 'http://web2:81/movies'
        lastId = int(albums[len(albums) - 1]['ID']) + 1
        new_movie = {
            'Title': album['Title'],
            'Genre': album['GenreOfMovie'],
            'Rating': album['Rating'],
            'Release date': album['ReleaseDate']
        }
        r = requests.post(url, json=new_movie)
        r = json.loads(r.text)
        new_alb = {
            'ID' :  str(lastId),
            'Album' : request.json['Album'],
            'Artist' : request.json['Artist'],
            'Genre' : request.json['Genre'],
            'Producer' : request.json['Producer'],
            'MovieID' : str(r['ID'])
        }
        albums.append(new_alb)
        return jsonify(new_alb), 201
    else:
        lastId = int(albums[len(albums) - 1]['ID']) + 1
        r = requests.get('http://web2:81/movies/'+request.json['MovieID'])
        if r.status_code == 404:
                return jsonify({'Error' : 'Album not found.'}), 404
        else:
            new_alb={
                    'ID' :  str(lastId),
                    'Album' : request.json['Album'],
                    'Artist' : request.json['Artist'],
                    'Genre' : request.json['Genre'],
                    'Producer' : request.json['Producer'],
                    'MovieID' : request.json['MovieID']
            }
            albums.append(new_alb)
            return jsonify(new_alb), 201

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
        return jsonify(update_album)

#using other web server
@app.route('/albums', methods=['GET'])
def getAllInfo():
    if(request.args.get('embedded', '') == "movie"):
            albumsEmb=copy.deepcopy(albums)
            for i in range(0, len(albums)):
                try:
                    r = requests.get('http://web2:81/movies/'+albumsEmb[int(i)]['MovieID'])
                    r = json.loads(r.text)
                    albumsEmb[int(i)]['MovieID'] = r
                except requests.exceptions.RequestException as e:
                    albumsEmb[int(i)]['MovieID'] = "null"
            return jsonify(albumsEmb), 200
    else:
        return jsonify(albums), 200

@app.route('/albums/<albumID>', methods=['GET'])
def getAlbum(albumID):
    if(request.args.get('embedded', '') == "movie"):
        albumsEmb=copy.deepcopy(albums)
        try:
            r = requests.get('http://web2:81/movies/'+albumsEmb[int(albumID)-1]['MovieID'])
            r = json.loads(r.text)
            albumsEmb[int(albumID)-1]['MovieID'] = r
        except requests.exceptions.RequestException as e:
            albumsEmb[int(albumID)-1]['MovieID'] = "null"
        return jsonify(albumsEmb[int(albumID)-1]), 200
    else:
        album_choose = [album for album in albums if album['ID'] == albumID]
        if len(album_choose) == 0:
                abort(404)
        album_choose = jsonify(album_choose)
        return album_choose 

@app.route('/albums/<albumID>/movie', methods=['PATCH'])
def changeMovie(albumID):
    album_choose = [album for album in albums if album['ID'] == albumID]
    if len(album_choose) == 0:
            abort(404)
    url = 'http://web2:81/movies/'+album_choose[0]['MovieID']
    r = requests.get(url)
    if r.status_code == 404:
        return jsonify({'Error' : 'Movie not found.'}), 404
    else:
        album_choose[0]["MovieID"] = request.json['MovieID']
        return jsonify(album_choose[0]), 200

@app.route('/albums/<albumID>/movie', methods=['PUT'])
def putMovie(albumID):
    album_choose = [album for album in albums if album['ID'] == albumID]
    if len(album_choose) == 0:
        abort(404)
    url = 'http://web2:81/movies/'+album_choose[0]['MovieID']
    change_movie = {
        'Title': request.json['Title'],
        'Genre': request.json['Genre'],
        'Rating': request.json['Rating'],
        'Release date': request.json['ReleaseDate']
    }
    r = requests.put(url, json=change_movie)
    r = r.text
    r = json.loads(r)
    return jsonify(r), 200

@app.route('/albums/<albumID>/movie', methods=['DELETE'])
def deleteMovie(albumID):
    album_choose = [album for album in albums if album['ID'] == albumID]
    if len(album_choose) == 0:
        abort(404)
    url = 'http://web2:81/movies/'+album_choose[0]['MovieID']
    r = requests.delete(url).text
    albums.remove(album_choose[0])
    r = json.loads(r)
    return albumID
#############SOAP################
class Album(ComplexModel):
	ID = Unicode
	Album = Unicode
	Artist = Unicode
	Genre = Unicode
	Producer = Unicode
	MovieID = Unicode

class Albums(ComplexModel):
	albums = Array(Album)
	
class AlbumsSoapService(spyne.Service):
	__soap_target_namespace__ = 'MyNS'
	__soap_server_address__ = '/soap/albums'
	__service_url_path__ = '/soap/albums'
	__in_protocol__ = Soap11(validator='lxml')
	__out_protocol__ = Soap11()

	@spyne.srpc(Unicode, Integer, _returns=Iterable(Album))
	def hello(str, cnt):
		for i in range(cnt):
			yield str

	@spyne.srpc(_returns=Array(Album))
	def getAlbumSoap():
		a = []
		for album in albums:
			a.append(Album(ID=album["ID"], Albums=album["Album"], Artist=album["Artist"], Genre=album["Genre"], Producer=album["Producer"], MovieID=album["MovieID"]))
		return a

    @spyne.srpc(Unicode, _returns=Array(Album))
    def getAlbumByIdSoap(Id):
        a = []
        for album in albums:
            if (album["ID"] == Id):
                a.append(Album(ID=album["ID"], Albums=album["Album"], Artist=album["Artist"], Genre=album["Genre"], Producer=album["Producer"], MovieID=album["MovieID"]))
        return a
        
if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True, port=5000)

