#!/usr/bin/env python

from base import UPnPServiceBase


class UPnPServiceDialReceiver(UPnPServiceBase):

    def __init__(self, ip, port="7678", config=None):
        super(UPnPServiceDialReceiver, self).__init__(ip, port)

        self.endpoint = '/RCR/control/dial'
        self.sns = "dial-multiscreen-org"
        self.stype = 'dial'

        if config is not None:
            self.endpoint = config['controlURL']

    def key_send(self, key_code, key_description = ''):
        action = 'SendKeyCode'
        args = [('KeyCode', key_code), ('KeyDescription', key_description)]

        response = self._send_cmd(action, args)

        result = self._get_result(response)

        return result

if __name__ == "__main__":
    s = UPnPServiceDialReceiver("192.168.0.100", "7678")

    print s.key_send('10146', '')