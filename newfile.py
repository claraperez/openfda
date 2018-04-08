import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?limit=10", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)

repo = repos['results']

print("The drug id is", repo[0]['openfda']['spl_id'])
print("The drug purpose is", repo[0]['purpose'])
print("The manufacturer name is", repo[0]['openfda']['manufacturer_name'])
print("The Ids for the rest of the drugs are:")
print("The drug id is", repo[1]['id'])
print("The drug id is", repo[2]['id'])
print("The drug id is", repo[3]['id'])
print("The drug id is", repo[4]['id'])
print("The drug id is", repo[5]['id'])
print("The drug id is", repo[6]['id'])
print("The drug id is", repo[7]['id'])
print("The drug id is", repo[8]['id'])
print("The drug id is", repo[9]['id'])