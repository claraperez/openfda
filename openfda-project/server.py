"""

Final Project Extension I: Description
In this first extension of the Final Project you must:
1. The listing and search of drugs must support a limit param with the
number of drugs to be collected from OpenFDA.
2. Add a new option to the web client to get a list with the warning of the
drugs. listWarnings must be the name of the resource in the web
server.

Final Project Extension II: Description
In this second extension of the Final Project you must:
If the HTML resource (page) requested by the Web Client is not
supported, send a 404 HTTP response code to the client and a web page
with a message describing it.

Final Project Extension III: Description
In this third extension of the Final Project the goal is to refactor the code to
use classes to improve the maintainability of the code. Three new classes
must be created:
1. OpenFDAClient: include the logic to communicate with the OpenFDA
remote API.
2. OpenFDAParser: includes the logic to extract the data from drugs
items.
3. OpenFDAHTML: includes the logic to the HTML visualization.

Final Project Extension IV: Description
In this fourth extension of the Final Project the goal is to add two thew
URLs:
http://localhost:8000/secret
The web server must sent to the client the status code 401
(Unauthorized) and the header WWW-Authenticate de basic Realm
http://localhost:8000/redirect
The web server must send to the client the status code 302 (Redirect)
and to redirect the client to the root web page (/) using the right header.

"""

import http.server
import socketserver
import http.client
import json

socketserver.TCPServer.allow_reuse_adress = True


class OpenFDAClient:
    # include the logic to communicate with the OpenFDA remote API.

    # Request from web page
    def r_webpage(request):

        if 'searchDrug' in request:

            if '\"' in request:
                if '&' in request:  # There's a limit in the request?
                    active_ingredient = request[request.index('=') + 1:request.index('&')]
                    #limit = request[request.index('&'):]
                    limit = '&limit=10'
                    query = '/drug/label.json?search=active_ingredient:' + active_ingredient
                    s_openfda = query + limit
                else:
                    active_ingredient = request[request.index('=') + 1:]
                    query = '/drug/label.json?search=active_ingredient:' + active_ingredient + '&limit=10'
                    s_openfda = query
            else:
                if '&' in request:  # There's a limit in the request?
                    active_ingredient = request[request.index('=') + 1:request.index('&')]
                    #limit = request[request.index('&'):]
                    limit = '&limit=10'
                    query = '/drug/label.json?search=active_ingredient:' + active_ingredient
                    s_openfda = query + limit
                else:
                    active_ingredient = request[request.index('=') + 1:]
                    query = '/drug/label.json?search=active_ingredient:"%s"' % active_ingredient + '&limit=10'
                    s_openfda = query


        elif 'searchCompany' in request:

            company = request[request.index('=') + 1:]
            query = '/drug/label.json?search=openfda.manufacturer_name:"%s"' % company + '&limit=10'
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
            s_openfda = "/drug/label.json?limit=10"

        print('request to openfda : ', s_openfda)
        return s_openfda

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

class OpenFDAParser:
    # includes the logic to extract the data from drugs items.
    def r_webclient(r_web, query_openfda, drugs):

        content = "<p>" + "Web request :" + r_web + "; Results for openFDA query : " + query_openfda + "</p>" + "<ul>"

        if 'listDrugs' in r_web:

            r_limit = r_web[r_web.index('?') + 1:]  # There's a limit in the request?
            s_limit = r_limit[r_limit.index('=') + 1:]  # the string with the limit number

            if not s_limit:  # There's no limit
                answer_webclient = 'drug id: ' + drugs['results'][0]['id']
                content = content + "<li>" + answer_webclient + "</li>" + "</ul>"
            else:
                i_limit = int(s_limit)

                for i in range(i_limit):
                    answer_webclient = 'drug id: ' + drugs['results'][i]['id']
                    content = content + "<li>" + answer_webclient + "</li>"
            content =  content + "</ul>"
            return content
        elif 'listCompanies' in r_web:
            i_limit = 10
            for i in range(i_limit):
                if (not drugs['results'][i]['openfda']) or (not drugs['results'][i]['openfda']['manufacturer_name']):
                    answer_webclient = 'drug_id:' + drugs['results'][i]['id'] + ' & ' 'company name: Unknown '
                else:
                    manufacturer_name = drugs['results'][i]['openfda']['manufacturer_name']

                    answer_webclient = 'drug_id:' + drugs['results'][i]['id'] + ' & ' 'company name: ' + \
                                   manufacturer_name[0]
                content = content + "<li>" + answer_webclient + "</li>"
            content = content + "</ul>"
            return content
        elif 'listWarnings' in r_web:

            i_limit = 10
            for i in range(i_limit):
                if 'warnings' in drugs['results'][i]:
                    warnings = drugs['results'][i]['warnings']
                    answer_webclient = 'drug_id:' + drugs['results'][i]['id'] + ' & ' + 'warnings: ' + warnings[0]
                    content = content + "<li>" + answer_webclient + "</li>"
                else:
                    warnings = drugs['results'][i]['warnings_and_cautions']
                    answer_webclient = 'drug_id:' + drugs['results'][i]['id'] + ' & ' + 'warnings: ' + warnings[0]
                    content = content + "<li>" + answer_webclient + "</li>"
            content = content + "</ul>"
            return content

        else:
            i_limit = 10
            for i in range(i_limit):
                answer_webclient = 'drug id: ' + drugs['results'][i]['id']
                content = content + "<li>" + answer_webclient + "</li>"
            content = content + "</ul>"
            return content


class OpenFDAHTML:
    # includes the logic to the HTML visualization.

    def visualizationHTML(r_web):
        if r_web == "/":
            # init, file to open search.html
            filename = "search.html"
            with open(filename, "r") as f:
                content = f.read()
            return content
        elif 'searchDrug' in r_web or 'searchCompany' in r_web or 'listDrugs' in r_web or 'listCompanies' in r_web \
                or 'listWarnings' in r_web:
            # init, file to open search.html
            filename = "search.html"
            with open(filename, "r") as f:
                content = f.read()

            # Read data from submitted form: label & limit
            print('request to fetch drugs')
            openfda_client = OpenFDAClient  # include the logic to communicate with the OpenFDA remote API.
            query_openfda = openfda_client.r_webpage(r_web)
            drugs = json.loads(openfda_client.openfda(query_openfda))

            if not 'error' in drugs:
                # Sending query results to OpenFDAParser
                openfda_parser = OpenFDAParser
                message = openfda_parser.r_webclient(r_web, query_openfda, drugs)
                content = content + str(message)
            else:  # error in query
                content = content + str(drugs)

            return content

        else:  # error 404
            # sending web page with error
            filename = "error404.html"
            with open(filename, "r") as f:
                content = f.read()
            return content


# ------------------------------------------------------------------------------------------------


PORT = 8000

# HTTPRequestHandler class
class serverRequestHandler(http.server.BaseHTTPRequestHandler):

    # GET
    def do_GET(self):

        r_web = self.path   #request from web page
        print(r_web)

        openfda_html = OpenFDAHTML  # includes the logic to the HTML visualization.

        if r_web == "/" or 'searchDrug' in r_web or 'searchCompany' in r_web or 'listDrugs' in r_web \
        or 'listCompanies' in r_web or 'listWarnings' in r_web:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
        elif 'secret' in r_web:
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'basic Realm')
        elif 'redirect' in r_web:
            self.send_response(302)
            self.send_header('Location', '/')
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Write content as utf-8 data
        content = openfda_html.visualizationHTML(r_web)
        self.wfile.write(bytes(content, "utf8"))

        return

# Handler = http.server.SimpleHTTPRequestHandler
Handler = serverRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)

httpd.serve_forever()
