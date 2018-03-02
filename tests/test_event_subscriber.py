from unittest import TestCase

from samsungtv.upnpevents import EventSubscriber


class TestEventSubscriber(TestCase):
    def test_subscribe(self):
        self.skipTest("Todo")

    # def test_real(self):
    #     # http SUBSCRIBE http://192.168.0.100:9197/dmr/upnp/event/RenderingControl1 TIMEOUT:1000 NT:'upnp:event'
    #
    #     s = EventSubscriber(u'http://192.168.0.100:9197/upnp/event/RenderingControl1')
    #
    #     result = s.subscribe()
    #     print result
    #
    #     # print s.renew(result['sid'])
    #     # print s.cancel(result['sid'])
    #
    #     pass
