from unittest import TestCase

from samsungtv.upnpservice import UPnPServiceConnectionManager


class TestUPnPServiceRendering(TestCase):
    def test_init(self):
        t = UPnPServiceConnectionManager('192.168.0.1')
        self.skipTest("Todo")

    # def test_real(self):
    #     import pprint
    #
    #     pprint.pprint("UPnPServiceConnectionManager")
    #     t = UPnPServiceConnectionManager('192.168.0.100', '9197')
    #
    #     conn = t.prepare_for_connection('http-get:*:image/jpeg:*')
    #
    #     print conn
    #
    #     # pprint.pprint(t.protocol_info())
    #     print t.connection_info()
    #     print t.connections()
    #
    #     # from avtransport import UPnPServiceAVTransport
    #     # av = UPnPServiceAVTransport('192.168.0.100', '9197', config={"controlURL":"/upnp/control/AVTransport1"})
    #     # print av.get_transport_info()
    #     # print av.get_stopped_reason()
    #     # print av.media_info()
    #     # print av.play()
    #     # print av.stop()
    #
    #     print t.connection_complete(conn["ConnectionID"])
