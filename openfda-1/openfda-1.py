import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET","/drug/label.json", None, headers)

r1 = conn.getresponse()
print(r1.status, r1.reason)
drugs_raw = r1.read().decode("utf-8")
conn.close()

drugs = json.loads(drugs_raw)

for result in drugs['results']:
    print('The drugs id is', result['id'])
    print('The drugs purpose is', result['purpose'])
    print('The drugs manufacturer name is', result['openfda']['manufacturer_name'])

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET","/drug/label.json?limit=10", None, headers)

r1 = conn.getresponse()
print(r1.status, r1.reason)
drugs_raw = r1.read().decode("utf-8")
conn.close()

drugs = json.loads(drugs_raw)

for result in drugs['results']:
    print('The drugs id is', result['id'])


