#!/usr/bin/env python

import base64
from base import UPnPServiceBase


class UPnPServiceWfaConfig(UPnPServiceBase):

    def __init__(self, ip, port="49152"):
        super(UPnPServiceWfaConfig, self).__init__(ip, port)

        self.endpoint = '/wps_control'
        self.stype = 'WFAWLANConfig'
        self.sns = "schemas-wifialliance-org"

    def get_device_info(self):
        action = 'GetDeviceInfo'
        args = []

        response = self._send_cmd(action, args)

        res = self._get_result(response)

        if res.get("faultcode"):
            raise Exception("Error {}".format(res.get("faultstring")), res.get("faultstring"))

        if not res.get("NewDeviceInfo"):
            raise Exception("Missing Device Info")

        return base64.b64decode(res['NewDeviceInfo'])
