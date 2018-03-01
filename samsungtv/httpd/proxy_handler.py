import mimetypes
import os
import shutil
from BaseHTTPServer import BaseHTTPRequestHandler
from urllib2 import urlopen


class ProxyHttpRequestHandler(BaseHTTPRequestHandler):

    dir_path = os.path.dirname(os.path.realpath(__file__)) + "/"

    def _send_ok(self):
        url = self.path[1:]  # replace '/'

        file = self.dir_path + "/" + url

        if os.path.exists(file) and os.path.isfile(file):
            f = open(file)
            content_type = mimetypes.guess_type(file)[0]

            f.close()
        elif url.startswith("http"):
            f = urlopen(url=url)
            content_type = f.info().getheaders("Content-Type")[0]

            f.close()
        else:
            self.send_response(404, "Not Found")
            self.send_header("X-App-Url", url)
            self.send_header("X-App-File", file)
            self.end_headers()
            return None

        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Type", content_type)
        self.send_header("X-App-Url", url)
        self.send_header("X-App-File", file)
        self.end_headers()

    def do_OPTIONS(self):
        self._send_ok()

    def do_HEAD(self):
        self._send_ok()

    def do_GET(self):
        url = self.path[1:]  # replace '/'

        file = self.dir_path + "/" + url

        if os.path.exists(file) and os.path.isfile(file):
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