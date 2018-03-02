import re
import sys
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from xml.etree import cElementTree

from collections import defaultdict


def etree_to_dict(t):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k: v[0] if len(v) == 1 else v for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v) for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d


class SubscribeHttpRequestHandler(BaseHTTPRequestHandler):
    NS = "{urn:schemas-upnp-org:event-1-0}"

    def do_NOTIFY(self):

        result = {}
        ip, _ = self.client_address

        content_len = int(self.headers.get('content-length', 0))
        data = self.rfile.read(content_len)

        # print "RAWWWWWWWWWWWWWWWWWWWWWWWWWWW"
        # print data

        properties = {}
        event = {}
        if data:
            doc = cElementTree.fromstring(data)

            for propnode in doc.findall('./{0}property'.format(self.NS)):
                for prop in propnode.getchildren():
                    # "Raw" Properties
                    properties[prop.tag] = prop.text

                    if prop.text is not None and prop.text.startswith("<"):
                        # // Extract Event
                        xml_string = re.sub(' xmlns="[^"]+"', '', prop.text, count=1)
                        pxml = cElementTree.fromstring(xml_string)
                        # pp = pxml.findall('./InstanceID/*')
                        # event = etree_to_dict(pp)

                        event = {}
                        for node in pxml.findall('./InstanceID/*'):
                            event[node.tag] = node.attrib

                    # print "--------------------------------------"
                    # print cElementTree.tostring(pxml)
                    # print cElementTree.tostring(pp)
                    # print etree_to_dict(pxml)
                    # print "--------------------------------------"

        result["ip"] = ip
        result["sid"] = self.headers.getheader("sid")
        result["nt"] = self.headers.getheader("nt")
        result["nts"] = self.headers.getheader("nts")
        result["event"] = event

        # result["raw"] = {
        # result["properties"] = properties
        #     "data": data,
        #     "headers": self.headers.items()
        # }

        self._log(result)

        response = "<html><body><h1>200 OK</h1></body></html>"

        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(response))
        self.send_header('Connection', 'close')
        self.end_headers()

        self.wfile.write(response.encode("UTF-8"))

    def do_OPTIONS(self):
        print "OPTIONS"
        self._success()

    def do_HEAD(self):
        print "HEAD"
        self._success()

    def do_GET(self):
        print "GET"
        self._success()

    def do_DELETE(self):
        print " DELETE"
        self._success()

    def do_PUT(self):
        print "PUT"
        self._success()

    def do_POST(self):
        print "POST"
        self._success()

    def _success(self):

        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    @staticmethod
    def _log(result):
        import pprint

        print " # ==================================="
        pprint.pprint(result)
        print ""

