#!/usr/bin/env python

from base import UPnPServiceBase

class UPnPServiceConnectionManager(UPnPServiceBase):

    def __init__(self, ip, port = "9197"):
        self.id = '0'
        self.ip = ip
        self.port = port
        self.endpoint = '/dmr/upnp/control/ConnectionManager1'
        self.stype='ConnectionManager'
        
        pass

    def protocol_info(self):

        action = 'GetProtocolInfo'
        args = [('InstanceID', self.id)]

        response = self._send_cmd(action, args)
    
        result = self._get_result(response)

        result['Sink'] = result['Sink'].split(",")
        
        return result

    def connection_info(self, id=0):

        action = 'GetCurrentConnectionInfo'
        args = [('ConnectionID', '0')]

        response = self._send_cmd(action, args)
    
        return self._get_result(response)

    def connections(self): 

        action = 'GetCurrentConnectionIDs'
        args = [('InstanceID', self.id)]

        response = self._send_cmd(action, args)
    
        return self._get_result(response)

if __name__ == "__main__":
    import pprint

    pprint.pprint("UPnPServiceConnectionManager \n")
    t = UPnPServiceConnectionManager('192.168.0.100', '9197')
    print t.connection_info()
    print t.connections()
    pprint.pprint(t.protocol_info()) 

