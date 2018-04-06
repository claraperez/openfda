import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET","/drugs/label.json", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
drugs_raw = r1.read().decode("utf-8")
conn.close()
print(drugs_raw)
drugs = json.loads(drugs_raw)
repo = drugs['results']
drug = repo[0]
drug_id = drug["id"]
print("The drug's id is", drug_id)

#print("The total number of repos", len(repo))
#print("The owner of the first repository is", repo['owner']['login'])

#for i in range(len(repos['results'])):
   # repo = repos[i]

   # print(repo["full_name"])