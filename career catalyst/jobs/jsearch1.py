import http.client

conn = http.client.HTTPSConnection("jsearch.p.rapidapi.com")

headers = {

}


res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))