List of albums

Running:
docker-compose build
docker-compose up -d

Terminal query examples:
1. GET the list of albums: curl -i http://193.219.91.104:4355/albums
2. GET the album by the album ID: curl -i http://193.219.91.104:4355/albums/1
3. GET the list of albums by genre: curl -i http://193.219.91.104:4355/albums/genre/Jazz
4. POST (add) a new album: 
curl -i -X POST -H "Content-Type: application/json" -d '{ "ID": "3", "Album": "Prelude", 
"Artist": "April", "Genre": "POP", "Producer": " "}' http://193.219.91.104:4355/albums
5. PUT (CHANGE) information about an album: 
curl -i -H "Content-type: application/json" -X PUT -d '{"Genre": "Pop"}' http://193.219.91.104:4355/albums/1
6. DELETE an album: curl -i -X DELETE http://193.219.91.104:4355/albums/1

Task Nr.2
_____________________________________________________________________________
7. GET information about albums with embedded every album's movie:
curl -i http://193.219.91.104:4355/albums?embedded=movie
8. GET information about album with specific ID with embedded album's movie:
curl -i http://193.219.91.104:4355/albums/1?embedded=movie
9. POST a new album with MovieID of existing movie:
curl -i -X POST -H "Content-Type: application/json" -d '{"Album" : "Who", "Artist" : "John", "Genre" : "POP", "Producer" : "Mark", "MovieID" : "2"}' http://193.219.91.104:4355/albums
10. POST a new album with embedded album's movie information:
curl -i -X POST -H "Content-Type: application/json" -d '{"Album" : "Who", "Artist" : "John", "Genre" : "POP", "Producer" : "Mark", "MovieID" : {"Title": "Home Alone", "GenreOfMovie": "Comedy", "Rating": "5", "ReleaseDate": "1997"}}' http://193.219.91.104:4355/albums?embedded=movie
11. PATCH to change album's movie ID:
curl -i -X PATCH -H "Content-Type: application/json" -d '{"MovieID": "10"}' http://193.219.91.104:4355/albums/1/movie
12. PUT (CHANGE) information about album's movie:
curl -i -H "Content-type: application/json" -X PUT -d '{"Title": "Best Movie", "Genre": "Comedy", "Rating": "7", "ReleaseDate": "2000"}' http://193.219.91.104:4355/albums/1/movie
13. DELETE album and it's movie:
curl -i -X DELETE http://193.219.91.104:4355/albums/1/movie
