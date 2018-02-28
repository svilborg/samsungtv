import getopt
import mimetypes
import os
import shutil
import sys
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urllib2 import urlopen


class HttpProxyServer(BaseHTTPRequestHandler):

    dir_path = os.path.dirname(os.path.realpath(__file__)) + "/"

    def response_success(self):
        url = self.path[1:]  # replace '/'

        file = self.dir_path + "/" + url

        if os.path.exists(file):
            f = open(file)
            content_type = mimetypes.guess_type(file)[0]

            f.close()
        elif url.startswith("http"):
            f = urlopen(url=url)
            content_type = f.info().getheaders("Content-Type")[0]

            f.close()
        else:
            self.send_response(404, "Not Found")
            self.end_headers()
            return None

        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Type", content_type)
        self.end_headers()

    def do_OPTIONS(self):
        self.response_success()

    def do_HEAD(self):
        self.response_success()

    def do_GET(self):
        url = self.path[1:]  # replace '/'

        file = self.dir_path + "/" + url
        
        if os.path.exists(file):
            f = open(file)
            content_type = mimetypes.guess_type(file)[0]
            size = os.path.getsize(file)
            name = os.path.basename(file)
        elif url.startswith("http"):
            f = urlopen(url=url)
            content_type = f.info().getheaders("Content-Type")[0]
            size = f.info().getheaders("Content-Length")[0]
            name = os.path.basename(url)
        else :
            self.send_response(404, "Not Found")
            self.end_headers()
            return None

        try:
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Disposition", 'attachment; filename="{}"'.format(name))
            self.send_header("Content-Length", str(size))
            self.end_headers()
            
            shutil.copyfileobj(f, self.wfile)
        finally:
            f.close()


def usage():
    print ""
    print "Usage: " + sys.argv[0] + " [OPTIONS]"
    print "  -h HOST"
    print "  -p Port"
    print ""


if __name__ == "__main__":

    host = ""
    port = 8000

    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:", ["host", "port"])
    except getopt.GetoptError, err:
        print(err)
        sys.exit(-1)

    for o, arg in opts:
        if o in ("-h", "--host"):
            host = arg
        elif o in ("-p", "--port"):
            port = int(arg)

        else:
            print "Unknown Options"

    try:
        HttpProxyServer.protocol_version = "HTTP/1.0"
        HttpProxyServer.dir_path = os.path.dirname(os.path.realpath(__file__)) + "/../media"

        httpd = HTTPServer((host, port), HttpProxyServer)
    
    except Exception as e:
        sys.stderr.write(str(e))
        sys.exit(-1)

    print "Serving on " + host + ":" + str(port) + " ... "

    while True:
        httpd.handle_request()
