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
        r_limit = request[request.index('&') + 1:]  # There's a limit in the request?
        s_limit = r_limit[r_limit.index('=') + 1:]  # the string with the limit number

        if not s_limit:  # There's no limit
            active_ingredient = request[request.index('=') + 1:]
            query = '/drug/label.json?search=active_ingredient:"%s"' % active_ingredient
            s_openfda = query

        else:
            active_ingredient = request[request.index('=') + 1:request.index('&')]
            limit = request[request.index('&'):]
            query = '/drug/label.json?search=active_ingredient:"%s"' % active_ingredient
            s_openfda = query + limit

    elif 'searchCompany' in request:

        company = request[request.index('=') + 1:]
        query = '/drug/label.json?search=openfda.manufacturer_name:"%s"' % company
        s_openfda = query

    elif 'listDrugs' in request:
        r_limit = request[request.index('?') + 1:]  # There's a limit in the request?
        s_limit = r_limit[r_limit.index('=') + 1:]  # the string with the limit number

        if not s_limit:  # There's no limit
            query = '/drug/label.json?'
            s_openfda = query

        else:
            limit = request[request.index('?') + 1:]
            query = '/drug/label.json?'
            s_openfda = query + limit

    else:
        s_openfda = "/drug/label.json?"

    return s_openfda


# Reply to web client

def r_webclient(r_web, drugs):
    if 'searchDrug' in r_web:
        l_active_ingredient = "<p>" + "Results for active ingredient request: " + r_web + "</p>" + "<ul>"
        r_limit = r_web[r_web.index('&') + 1:]  # There's a limit in the request?
        s_limit = r_limit[r_limit.index('=') + 1:]  # the string with the limit number

        if not s_limit:  # There's no limit
            answer_webclient = drugs['results'][0]['id']  # result list with only one element (dictionary), index=0
            l_active_ingredient = l_active_ingredient + "<li>" + 'drug id: ' + answer_webclient + "</li>" + "</ul>"
        else:
            i_limit = int(s_limit)
            for i in range(i_limit):
                answer_webclient = drugs['results'][i]['id']
                l_active_ingredient = l_active_ingredient + "<li>" + 'drug id: ' + answer_webclient + "</li>"
            l_active_ingredient = l_active_ingredient + "</ul>"

        return l_active_ingredient

    elif 'searchCompany' in r_web:
        l_company = "<p>" + "Results for company request: " + r_web + "</p>" + "<ul>"
        generic_name = drugs['results'][0]['openfda']['generic_name']  # result list with only one element, index=0
        brand_name = drugs['results'][0]['openfda']['brand_name']  # result list with only one element, index=0
        answer_webclient = 'generic_name:' + generic_name[0] + ' & ' 'brand_name: ' + brand_name[0]
        l_company = l_company + "<li>" + answer_webclient + "</li>" + "</ul>"

        return l_company


    elif 'listDrugs' in r_web:
        l_listdrugs = "<p>" + "Results for list drugs request: " + r_web + "</p>" + "<ul>"
        r_limit = r_web[r_web.index('?') + 1:]  # There's a limit in the request?
        s_limit = r_limit[r_limit.index('=') + 1:]  # the string with the limit number

        if not s_limit:  # There's no limit
            answer_webclient = 'drug id: ' + drugs['results'][0]['id']
            l_listdrugs = l_listdrugs + "<li>" + answer_webclient + "</li>" + "</ul>"
        else:
            i_limit = int(s_limit)
            for i in range(i_limit):
                answer_webclient = 'drug id: ' + drugs['results'][i]['id']
                l_listdrugs = l_listdrugs + "<li>" + answer_webclient + "</li>"
            l_listdrugs = l_listdrugs + "</ul>"

        return l_listdrugs



    elif 'listCompanies' in r_web:
        l_companies = "<p>" + "Results for list companies request: " + r_web + "</p>" + "<ul>"
        # check for company, caution openfda in results might be empty {}
        if (not drugs['results'][0]['openfda']) or (not drugs['results'][0]['openfda']['manufacturer_name']):
            answer_webclient = 'drug_id:' + drugs['results'][0]['id'] + ' & ' 'company name: Unknown '
        else:
            manufacturer_name = drugs['results'][0]['openfda']['manufacturer_name']
            answer_webclient = 'drug_id:' + drugs['results'][0]['id'] + ' & ' 'company name: ' + manufacturer_name[0]
        l_companies = l_companies + "<li>" + answer_webclient + "</li>" + "</ul>"

        return l_companies

    elif 'listWarnings' in r_web:
        l_warnings = "<p>" + "Results for list warnings request: " + r_web + "</p>" + "<ul>"
        generic_name = drugs['results'][0]['openfda']['generic_name']
        warnings = drugs['results'][0]['warnings']
        answer_webclient = 'generic_name:' + generic_name[0] + ' & ' + 'warnings: ' + warnings[0]
        l_warnings = l_warnings + "<li>" + answer_webclient + "</li>" + "</ul>"

        return l_warnings


# HTTPRequestHandler class
class serverRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):

        r_web = self.path  # request from web page
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

        elif 'searchDrug' in r_web or 'searchCompany' in r_web or 'listDrugs' in r_web or 'listCompanies' in r_web \
                or 'listWarnings' in r_web:

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

            # Read data from submitted form: label & limit
            print('request to fetch drugs')
            r_openfda = r_webpage(r_web)

            # sending request openFDA
            drugs = json.loads(openfda(r_openfda))  # 'results' in drugs is a list with a dictionary

            if not 'error' in drugs:
                # Sending query results to openFDA web client
                message = r_webclient(r_web, drugs)
                self.wfile.write(bytes(str(message), "utf8"))
            else:  # error in query
                self.wfile.write(bytes(str(drugs), "utf8"))

        else:  # error 404
            """
            # sending message to client
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

            message = 'The HTML resource (page) requested by the Web Client is not supported,404 HTTP response code '
            self.wfile.write(bytes(str(message), "utf8"))

            """

            # sending web page with error

            filename = "error404.html"
            with open(filename, "r") as f:
                content = f.read()
            # Send response status code
            self.send_response(200)
            # Send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # Write content as utf-8 data
            self.wfile.write(bytes(content, "utf8"))

        return


# Handler = http.server.SimpleHTTPRequestHandler
Handler = serverRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)

httpd.serve_forever()
