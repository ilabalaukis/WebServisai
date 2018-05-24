from suds.client import Client as SudsClient
url = 'http://localhost/soap/albums?wsdl'
client = SudsClient(url=url, cache=None)
r = client.service.getAlbumSoap()
print r
