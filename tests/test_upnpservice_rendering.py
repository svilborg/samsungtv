from unittest import TestCase

from samsungtv.upnpservice import UPnPServiceRendering


class TestUPnPServiceRendering(TestCase):
    def test_init(self):
        t = UPnPServiceRendering('192.168.0.1')
        self.skipTest("Todo")


    # def test_real(self):
    #     print "UPnPServiceRendering \n"
    #
    #     t = UPnPServiceRendering('192.168.0.100', '9197')
    #     # print t.audio_selection()
    #     # print t.video_selection()
    #     print t.volume()
    #     # print t.tv_slide_show()
    #     # print t.set_tv_slide_show(0,'2')
    #     # print t.zoom(0, 0 , 350, 620)
    #     # print t.presets()
    #     # print t.select_preset()


    # def test_real_moving_pic(self):
    #     import time
    #
    #     # https://i.imgur.com/BMvDxow.jpg
    #     # 3847x808
    #     t = UPnPServiceRendering('192.168.0.100', '9197')
    #
    #     x = 0
    #     y = 20
    #     w = 800
    #     h = 360
    #
    #     while True:
    #         time.sleep(0.1)
    #         print t.zoom(x, y, w, h)
    #
    #         # start +=10
    #         x += 3
    #         print (x, y, w, h)
    #         # y +=10
    #         pass
