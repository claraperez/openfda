
import http.server
import socketserver
import http.client
import json


PORT = 8002

# HTTPRequestHandler class
class serverRequestHandler(http.server.BaseHTTPRequestHandler):

    # GET
    def do_GET(self):

        r_web = self.path   #request from web page
        print(r_web)

        if 'label' in r_web or 'limit' in r_web:
            print("if label")
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
            r_openfda = r_web[r_web.index('?') + 1:]  # print(s[s.index('.')+1:])
            print(r_openfda)
            label = r_web[r_web.index('=') + 1:r_web.index('&')]
            print(label)
            limit = r_web[r_web.index('&'):]
            print(limit)
            # string for openfda query
            s_openfda = "/drug/label.json?search=generic_name:" + label + limit
            print(s_openfda)

            # sending request openFDA

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", s_openfda, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

            drugs = json.loads(repos_raw)
            self.wfile.write(bytes(str(drugs), "utf8"))


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




        return

# Handler = http.server.SimpleHTTPRequestHandler
Handler = serverRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()
