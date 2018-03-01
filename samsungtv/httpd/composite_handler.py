from BaseHTTPServer import HTTPServer

import sys
import os

from proxy_handler import ProxyHttpRequestHandler
from subscribe_handler import SubscribeHttpRequestHandler


class CompositeHttpRequestHandler(ProxyHttpRequestHandler, SubscribeHttpRequestHandler):
    pass


if __name__ == "__main__":

    host = ""
    port = 8008

    try:
        CompositeHttpRequestHandler.dir_path = os.path.dirname(os.path.realpath(__file__)) + "/../media"
        httpd = HTTPServer((host, port), CompositeHttpRequestHandler)

    except Exception as e:
        sys.stderr.write(str(e))
        sys.exit(-1)

    print "Serving on " + host + ":" + str(port) + " ... "

    while True:
        try:
            httpd.handle_request()
        except KeyboardInterrupt as e1:
            print "Bye"
            sys.exit(0)
