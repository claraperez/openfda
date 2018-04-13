import http.server
import socketserver
import json

PORT = 8002

# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        headers = {'User-Agent': 'http-client'}

        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET",'/drug/label.json?limit=10', None, headers)

        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        drugs_raw = r1.read().decode("utf-8")
        conn.close()

        drugs = json.loads(drugs_raw)


        drugs= drugs['results']
        drugs_id =  "<ol>" + drugs[0]['id'] + "</ol>"
        for i in range(9):
            drugs_id = drugs_id + "<ol>" + drugs[i+1]['id'] + "</ol>"
        
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send message back to client
        message = drugs_id
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return

# Handler = http.server.SimpleHTTPRequestHandler
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()

