#!/usr/bin/env python
import xml.etree.cElementTree as XML
from base import UPnPServiceBase


class UPnPServiceAVTransport(UPnPServiceBase):

    SEEK_UNITS = [
        "TRACK_NR",
        "REL_TIME",
        "ABS_TIME",
        "ABS_COUNT",
        "REL_COUNT",
        "X_DLNA_REL_BYTE",
        "FRAME",
    ]

    def __init__(self, ip, port="9197", id='0', config=None):
        super(UPnPServiceAVTransport, self).__init__(ip, port)

        self.id = id
        self.stype = 'AVTransport'
        self.endpoint = ''

        if config is not None:
            self.endpoint = config['controlURL']

    def url(self, uri):
        action = 'SetAVTransportURI'
        args = [('InstanceID', self.id),
                ('CurrentURI', uri),
                ('CurrentURIMetaData', '')
                # ('CurrentURIMetaData', '&lt;DIDL-Lite xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/" xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:sec="http://www.sec.co.kr/"&gt;&lt;item id="f-0" parentID="0" restricted="0"&gt;&lt;dc:title&gt;Video&lt;/dc:title&gt;&lt;dc:creator&gt;vGet&lt;/dc:creator&gt;&lt;upnp:class&gt;object.item.videoItem&lt;/upnp:class&gt;&lt;res protocolInfo="http-get:*:video/mp4:DLNA.ORG_OP=01;DLNA.ORG_CI=0;DLNA.ORG_FLAGS=01700000000000000000000000000000" sec:URIType="public"&gt;$URI&lt;/res&gt;&lt;/item&gt;&lt;/DIDL-Lite&gt;')
                ]

        response = self._send_cmd(action, args)

        return self._get_result(response)

    def set_url(self, uri):
        action = 'SetAVTransportURI'
        args = [
            ('InstanceID', self.id),
            ('CurrentURI', uri),
            ('CurrentURIMetaData', '')
        ]

        response = self._send_cmd(action, args)

        return self._get_result(response)

    def set_next_url(self, uri):
        action = 'SetNextAVTransportURI'
        args = [
            ('InstanceID', self.id),
            ('NextURI', uri),
            ('NextURIMetaData', '')
        ]

        response = self._send_cmd(action, args)

        return self._get_result(response)

    def prefetch_url(self, uri):
        action = 'X_PrefetchURI'
        args = [
            ('InstanceID', self.id),
            ('PrefetchURI', uri),
            ('PrefetchURIMetaData', '')
        ]

        response = self._send_cmd(action, args)
        # print response
        return self._get_result(response)

    def get_transport_settings(self):
        action = 'GetTransporget_transport_settings'
        args = [('InstanceID', self.id)]

        response = self._send_cmd(action, args)

        return self._get_result(response)

    def device_cap(self):
        action = 'GetDeviceCapabilities'
        args = [('InstanceID', self.id)]

        response = self._send_cmd(action, args)

        return self._get_result(response)

    def player_app_hint(self):
        action = 'X_PlayerAppHint'
        args = [('InstanceID', self.id)]

        response = self._send_cmd(action, args)

        return self._get_result(response)

    def get_transport_info(self):
        action = 'GetTransportInfo'
        args = [('InstanceID', self.id)]

        response = self._send_cmd(action, args)

        return self._get_result(response)

    def media_info(self):
        action = 'GetMediaInfo'
        args = [('InstanceID', self.id)]

        response = self._send_cmd(action, args)

        return self._get_result(response)

    def play(self, speed="1"):
        action = 'Play'
        args = [('InstanceID', self.id), ('Speed', speed)]

        response = self._send_cmd(action, args)

        return self._get_result(response)

    def pause(self, speed="1"):
        action = 'Pause'
        args = [('InstanceID', self.id), ('Speed', speed)]

        response = self._send_cmd(action, args)

        return self._get_result(response)

    def stop(self):
        action = 'Stop'
        args = [('InstanceID', self.id)]

        response = self._send_cmd(action, args)

        return self._get_result(response)

    def next(self):
        action = 'Next'
        args = [('InstanceID', self.id)]

        response = self._send_cmd(action, args)

        return self._get_result(response)

    def previous(self):
        action = 'Previous'
        args = [('InstanceID', self.id)]

        response = self._send_cmd(action, args)

        return self._get_result(response)

    def get_position_info(self):
        action = 'GetPositionInfo'
        args = [('InstanceID', self.id)]

        response = self._send_cmd(action, args)

        result = self._get_result(response)

        metadata = result['TrackMetaData']

        if metadata and metadata != '':
            xml = XML.fromstring(metadata)
            title = xml.findtext('.//{http://purl.org/dc/elements/1.1/}title')
            artist = xml.findtext('.//{http://purl.org/dc/elements/1.1/}creator')
            # uri = xml.findtext('.//{urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/}res')

            result['metadata'] = {'title': title, 'artist': artist}

        return result

    def seek(self, unit='TRACK_NR', target=1):

        action = 'Seek'
        args = [('InstanceID', self.id), ('Unit', unit), ('Target', target)]

        response = self._send_cmd(action, args)

        return self._get_result(response)

    def get_stopped_reason(self):
        action = 'X_GetStoppedReason'
        args = [('InstanceID', self.id)]

        response = self._send_cmd(action, args)

        return self._get_result(response)

    def get_current_transport_actions(self):
        action = 'GetCurrentTransportActions'
        args = [('InstanceID', self.id)]

        response = self._send_cmd(action, args)

        return self._get_result(response)
