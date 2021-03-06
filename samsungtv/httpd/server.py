import getopt
import os
import sys
from BaseHTTPServer import HTTPServer

from composite_handler import CompositeHttpRequestHandler

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
        CompositeHttpRequestHandler.dir_path = os.curdir + "/media"
        # CompositeHttpRequestHandler.dir_path = os.path.dirname(os.path.realpath(__file__)) + "/../media"
        httpd = HTTPServer((host, port), CompositeHttpRequestHandler)

    except Exception as e:
        sys.stderr.write(str(e))
        sys.exit(-1)

    print "Serving on " + host + ":" + str(port) + " ... "

    while True:
        httpd.handle_request()
