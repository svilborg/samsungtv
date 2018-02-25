#!/usr/bin/env python

import base64
from base import UPnPServiceBase

class UPnPServiceWfaConfig(UPnPServiceBase):

    def __init__(self, ip, port = "49152"):
        self.ip = ip
        self.port = port
        self.endpoint = '/wps_control'
        self.stype ='WFAWLANConfig'

        pass

    def get_device_info(self):

        action = 'GetDeviceInfo'
        args = []

        response = super(UPnPServiceWfaConfig, self)._send_cmd(action, args)
    
        res = super(UPnPServiceWfaConfig, self)._get_result(response)
        
        return base64.b64decode(res['NewDeviceInfo'])


if __name__ == "__main__":

    print "UPnPServiceWfaConfig \n"
    t = UPnPServiceWfaConfig('192.168.0.1')

    print t.get_device_info()

