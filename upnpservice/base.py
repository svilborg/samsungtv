#!/usr/bin/env python
import re
import requests
import xml.etree.cElementTree as XML


class UPnPServiceBase(object):
    soap_body_template = (
        '<?xml version="1.0"?>'
        '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"'
        ' s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'
        '<s:Body>'
        '<u:{action} xmlns:u="urn:{sns}:service:'
        '{stype}:{version}">'
        '{arguments}'
        '</u:{action}>'
        '</s:Body>'
        '</s:Envelope>')

    def __init__(self, ip, port="9197"):
        self.endpoint = ""
        self.stype = ""
        self.ip = ip
        self.port = port

    def _is_error(self, response):
        m = re.match(r".*errorCode.*", response)

        return True if m else False

    def _get_result(self, response):
        if self._is_error(response):
            return self._parse_error(response)

        tree = XML.fromstring(response)
        body = tree.find("{http://schemas.xmlsoap.org/soap/envelope/}Body")[0]

        res = {}
        for i in body:
            res[i.tag] = i.text

        return res

    def _send_cmd(self, action, arguments):

        args = ''
        for tag, value in arguments:
            args += '<{tag}>{value}</{tag}>'.format(tag=tag, value=value)

        sns = "schemas-upnp-org"
        # sns = "schemas-wifialliance-org"
        # sns = "dial-multiscreen-org"

        soap_action = '"urn:{sns}:service:{stype}:{version}#{action}"'.format(
            sns=sns,
            stype=self.stype,
            version="1",
            action=action)

        headers = {
            'Content-Type': 'text/xml',
            'SOAPAction': soap_action
        }

        data = self.soap_body_template.format(
            sns=sns,
            arguments=args,
            action=action,
            stype=self.stype,
            version=1)

        # print "=================================="
        # print headers
        # print "=================================="
        # print data
        # print "=================================="
        
        r = requests.post('http://' + self.ip + ':' + str(self.port) + self.endpoint, data=str(data), headers=headers)
        return r.content

    def _parse_error(self, response):
        """ Parse an error returned from the Sonos speaker.
        """
        error = XML.fromstring(response)
        error_code = error.findtext('.//{urn:schemas-upnp-org:control-1-0}errorCode')
        error_message = error.findtext('.//{urn:schemas-upnp-org:control-1-0}errorDescription')

        if error_code is not None:
            raise Exception(error_message, error_code)
        else:
            raise Exception('Unknown Error ' + response, 0)

