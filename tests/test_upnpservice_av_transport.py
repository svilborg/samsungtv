from unittest import TestCase
from samsungtv.upnpservice import UPnPServiceAVTransport

class TestUPnPServiceAVTransport(TestCase):

    def test_init(self):
        t = UPnPServiceAVTransport('192.168.0.1')
        self.skipTest("Todo")

    # def test_real(self):
    #     print "UPnPServiceAVTransport \n"
    #
    #     import pprint
    #     import time
    #
    #     t = UPnPServiceAVTransport('192.168.0.100', '9197', config={'controlURL': '/dmr/upnp/control/AVTransport1'})

        # print "===================="
        # pprint.pprint(t.device_cap())

        # print "===================="
        # pprint.pprint(t.get_transport_info())
        # print "===================="
        # pprint.pprint(t.get_transport_settings())


        # print t.set_url("http://192.168.0.103:8000/media/t.mp4")
        # print t.set_url("http://192.168.0.103:8000/media/test.jpg#1")
        # print t.set_next_url("http://192.168.0.103:8000/media/test2.jpg#2")
        # time.sleep(1)

        # print "===================="
        # print t.play()

        # print "===================="
        # pprint.pprint (t.get_position_info())

        # time.sleep(2)
        # print "===================="

        # time.sleep(4)
        # print "===================="
        # print t.pause()

        # print "===================="
        # pprint.pprint(t.media_info())

        # time.sleep(4)
        # print t.next()

        # print "===================="
        # pprint.pprint(t.media_info())

        # exit(1)

        # # print t.set_url("http://192.168.0.103:8000/media/test.jpg")
        # # print t.set_next_url("http://192.168.0.103:8000/media/test3.jpg")
        # # print t.seek('REL_TIME', '00:00:05')

        # # print t.prefetch_url("http://192.168.0.103:8000/media/test3.jpg")
        # # print t.stop()

    # def test_real_pic_rotate (self) :
    #     l = [
    #     'http://i.imgur.com/6yHmlwT.jpg',
    #     'http://i.imgur.com/qCoybZR.jpg',
    #     'http://i.imgur.com/hl4mfZf.jpg',
    #     ]
    #
    #     is_play=False
    #
    #     for img in l:
    #
    #         print img
    #
    #         if not is_play:
    #             print t.set_url(img)
    #             print t.play()
    #
    #             is_play=True
    #
    #             time.sleep(1)
    #
    #         else:
    #             print t.set_next_url(img)
    #             print t.next()
    #
    #         time.sleep(5)
    #     pprint.pprint (t.get_transport_info())
    #     exit(1)
