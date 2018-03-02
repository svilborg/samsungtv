from unittest import TestCase

from samsungtv.upnpservice import UPnPServiceWfaConfig


class TestUPnPServiceWfaConfig(TestCase):
    def test_get_device_info(self):
        t = UPnPServiceWfaConfig('192.168.0.1')
        self.skipTest("Todo")

    # def test_real(self):
    #     print "UPnPServiceWfaConfig \n"
    #     t = UPnPServiceWfaConfig('192.168.0.1')
    #
    #     print t.get_device_info()


#
# class TestUPnPServiceAVTransport(TestCase):
#     def test_init(self):
#         t = UPnPServiceAVTransport('192.168.0.1')
#         self.skipTest("Todo")
#
# # def test_real(self):
