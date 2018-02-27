import getopt
import mimetypes
import os
import shutil
import sys
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urllib2 import urlopen


class HttpProxyServer(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        print format
        print args
        pass

    def log_request(self, code='-', size='-'):
        print code
        pass

    def response_success(self):
        url = self.path[1:]  # replace '/'

        if os.path.exists(url):
            f = open(url)
            content_type = mimetypes.guess_type(url)[0]
        else:
            f = urlopen(url=url)

            content_type = f.info().getheaders("Content-Type")[0]

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

        content_type = ''
        if os.path.exists(url):
            f = open(url)
            content_type = mimetypes.guess_type(url)[0]
            size = os.path.getsize(url)
        elif not url or not url.startswith('http'):
            self.response_success()
            return
        else:
            f = urlopen(url=url)

        try:
            if not content_type:
                # content_type = f.info().getheaders("Content-Type")[0]
                size = f.info().getheaders("Content-Length")[0]

            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Disposition", 'attachment; filename="{}"'.format(os.path.basename(url)))
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
        httpd = HTTPServer((host, port), HttpProxyServer)
    except Exception as e:
        # print e
        sys.stderr.write(str(e))
        sys.exit(-1)

    print "Serving on " + host + ":" + str(port) + " ... "

    while True:
        httpd.handle_request()
