import socket

class DialService(object):

    def __init__(self, ip, port = "9197"):
        self.ip = ip
        self.port = port
        pass

    def _get_response(self, response):
        headers, addr = response
   
        result = {
            'ip' : addr[0],
            'port' : addr[1]
        }

        for s in headers.splitlines():
            x = s.split(": ")
            if len(x) == 2:
                result[x[0].lower()] = x[1]    
        return result
