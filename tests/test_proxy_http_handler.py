import sys
from BaseHTTPServer import HTTPServer
from unittest import TestCase

from samsungtv.httpd.proxy_handler import ProxyHttpRequestHandler


class TestProxyHttpRequestHandler(TestCase):
    def test__log(self):
        self.skipTest("Todo")

    # def test_real(self):
    #     host = ""
    #     port = 8007
    #
    #     try:
    #         # SubscribeRequestHandler.protocol_version = "HTTP/1.0"
    #
    #         httpd = HTTPServer((host, port), ProxyHttpRequestHandler)
    #
    #     except Exception as e:
    #         sys.stderr.write(str(e))
    #         sys.exit(-1)
    #
    #     print "Serving on " + host + ":" + str(port) + " ... "
    #
    #     while True:
    #         httpd.handle_request()
