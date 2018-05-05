import http.server
import socketserver
import http.client
import json

socketserver.TCPServer.allow_reuse_adress = True
PORT = 8000

# Function openFDA requests
def openfda(query_openfda):

    # sending request openFDA

    headers = {'User-Agent': 'http-client'}
    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", query_openfda, None, headers)
    r1 = conn.getresponse()
    print(r1.status, r1.reason)
    repos_raw = r1.read().decode("utf-8")
    conn.close()
    return repos_raw

# Request from web page
def r_webpage(request):

    if 'searchDrug' in request:

        active_ingredient = request[request.index('=') + 1:]
        query = '/drug/label.json?search=active_ingredient:"%s"' %active_ingredient
        s_openfda = query

    elif 'searchCompany' in request:

        company = request[request.index('=') + 1:]
        query = '/drug/label.json?search=openfda.manufacturer_name:"%s"' %company
        s_openfda = query

    else:

        s_openfda = "/drug/label.json?"

    return s_openfda

# HTTPRequestHandler class
class serverRequestHandler(http.server.BaseHTTPRequestHandler):

    # GET
    def do_GET(self):

        r_web = self.path   #request from web page
        print(r_web)

        if r_web == "/":
            # init, file to open search.html
            filename = "search.html"
            with open(filename, "r") as f:
                content = f.read()
            # Send response status code
            self.send_response(200)
            # Send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # Write content as utf-8 data
            self.wfile.write(bytes(content, "utf8"))

        else:

            # init, file to open search.html
            filename = "search.html"
            with open(filename, "r") as f:
                content = f.read()
            # Send response status code
            self.send_response(200)
            # Send headers
            self.send_header('Content-type','text/html')
            self.end_headers()
            # Write content as utf-8 data
            self.wfile.write(bytes(content, "utf8"))

            # Read data from submitted form: label & limit
            print('request to fetch drugs')
            r_openfda = r_webpage(r_web)

            # sending request openFDA
            drugs = json.loads(openfda(r_openfda))  # 'results' in drugs is a list with a dictionary

            if not 'error' in drugs:
                # Sending query results to openFDA web client
                if 'searchDrug' in r_web:
                    l_active_ingredient = "<p>" + "Results for active ingredient request: " + r_web + "</p>" + "<ul>"
                    answer_webclient = drugs['results'][0]['id']  # result list with only one element (dictionary), index=0
                    l_active_ingredient = l_active_ingredient + "<li>" + 'drug id: ' + answer_webclient + "</li>" + "</ul>"
                    self.wfile.write(bytes(str(l_active_ingredient), "utf8"))

                elif 'searchCompany' in r_web:
                    l_company = "<p>" + "Results for company request: " + r_web + "</p>" + "<ul>"
                    generic_name = drugs['results'][0]['openfda']['generic_name']  # result list with only one element, index=0
                    brand_name = drugs['results'][0]['openfda']['brand_name']  # result list with only one element, index=0
                    answer_webclient = 'generic_name:' + generic_name[0] + ' & ' 'brand_name: ' + brand_name[0]
                    l_company = l_company + "<li>" + answer_webclient + "</li>" + "</ul>"
                    self.wfile.write(bytes(str(l_company), "utf8"))

                elif 'listDrugs' in r_web:
                    l_listdrugs = "<p>" + "Results for list drugs request: " + r_web + "</p>" + "<ul>"
                    generic_name = drugs['results'][0]['openfda']['generic_name']
                    answer_webclient = 'generic_name:' + generic_name[0] + ' & ' + 'drug id: ' + drugs['results'][0]['id']
                    l_listdrugs = l_listdrugs + "<li>" + answer_webclient + "</li>" + "</ul>"
                    self.wfile.write(bytes(str(l_listdrugs), "utf8"))

                elif 'listCompanies'in r_web:
                    l_companies = "<p>" + "Results for list companies request: " + r_web + "</p>" + "<ul>"
                    # check for company, caution openfda in results might be empty {}
                    if (not drugs['results'][0]['openfda']) or (not drugs['results'][0]['openfda']['manufacturer_name']):
                        answer_webclient = 'drug_id:' + drugs['results'][0]['id'] + ' & ' 'company name: Unknown '
                    else:
                        manufacturer_name = drugs['results'][0]['openfda']['manufacturer_name']
                        answer_webclient = 'drug_id:' + drugs['results'][0]['id'] + ' & ' 'company name: ' + \
                                           manufacturer_name[0]
                    l_companies = l_companies + "<li>" + answer_webclient + "</li>" + "</ul>"
                    self.wfile.write(bytes(str(l_companies), "utf8"))
            else:   # error in query
                self.wfile.write(bytes(str(drugs), "utf8"))



        return

# Handler = http.server.SimpleHTTPRequestHandler
Handler = serverRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)

httpd.serve_forever()
