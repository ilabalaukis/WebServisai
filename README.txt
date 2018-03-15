List of albums

Running:
docker-compose up -d

Terminal query examples:
1. GET the list of albums: curl -i localhost/albums/
2. GET the songs of an album: curl -i localhost/albums/album/1
3. POST (add) a new album: 
curl -i -X POST -H "Content-Type: application/json" -d '{ "ID": "3", "Album": "Prelude", 
"Artist": "April", "Genre": "K-pop, dance", "Producer": " "}' localhost/albums/
4. PUT (CHANGE) information about an album: 
curl -i -H "Content-type: application/json" -X PUT -d '{"Genre": "Pop"}' localhost/albums/1
5. DELETE an album: curl -i -X DELETE localhost/albums/1
