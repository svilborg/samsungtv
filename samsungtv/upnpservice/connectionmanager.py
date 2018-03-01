#!/usr/bin/env python

from base import UPnPServiceBase


class UPnPServiceConnectionManager(UPnPServiceBase):

    def __init__(self, ip, port="9197", config=None):
        super(UPnPServiceConnectionManager, self).__init__(ip, port)

        self.id = '0'
        self.stype = 'ConnectionManager'
        self.endpoint = '/dmr/upnp/control/ConnectionManager1'

        if config is not None:
            self.endpoint = config['controlURL']

    def protocol_info(self):
        action = 'GetProtocolInfo'
        args = [('InstanceID', self.id)]

        response = self._send_cmd(action, args)

        result = self._get_result(response)

        result['Sink'] = result['Sink'].split(",")

        return result

    def connection_info(self):
        action = 'GetCurrentConnectionInfo'
        args = [('ConnectionID', '0')]

        response = self._send_cmd(action, args)

        return self._get_result(response)

    def connections(self):
        action = 'GetCurrentConnectionIDs'
        args = [('InstanceID', self.id)]

        response = self._send_cmd(action, args)

        return self._get_result(response)

    def prepare_for_connection(self, proto="", pcm="", pc_id="-1", d="Input"):
        action = 'PrepareForConnection'
        args = [
            ('RemoteProtocolInfo', proto),
            ('PeerConnectionManager', pcm),
            ('PeerConnectionID', pc_id),
            ('Direction', d)
        ]

        response = self._send_cmd(action, args)

        return self._get_result(response)

    def connection_complete(self, con_id="0"):
        action = 'ConnectionComplete'
        args = [
            ('ConnectionID', con_id)
        ]

        response = self._send_cmd(action, args)

        return self._get_result(response)


if __name__ == "__main__":
    import pprint

    pprint.pprint("UPnPServiceConnectionManager")
    t = UPnPServiceConnectionManager('192.168.0.100', '9197')

    conn = t.prepare_for_connection('http-get:*:image/jpeg:*')

    print conn

    # pprint.pprint(t.protocol_info())
    print t.connection_info()
    print t.connections()

    from avtransport import UPnPServiceAVTransport

    # av = UPnPServiceAVTransport('192.168.0.100', '9197', config={"controlURL":"/upnp/control/AVTransport1"})
    # print av.get_transport_info()
    # print av.get_stopped_reason()
    # print av.media_info()
    # print av.play()
    # print av.stop()

    print t.connection_complete(conn["ConnectionID"])
