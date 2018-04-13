import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET",'/drug/label.json?search=openfda.generic_name:"ASPIRIN"&count=openfda.manufacturer_name.exact', None, headers)

r1 = conn.getresponse()
print(r1.status, r1.reason)
drugs_raw = r1.read().decode("utf-8")
conn.close()

drugs = json.loads(drugs_raw)
for term in drugs['results']:
    print('The manufacturer that produces aspirin is', term['term'])
