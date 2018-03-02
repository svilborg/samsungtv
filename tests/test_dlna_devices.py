from unittest import TestCase

from samsungtv.dlna import DlnaDevice, DlnaDevices


class TestDlnaDevices(TestCase):
    def test_get_devices(self):
        self.skipTest("Todo")

    # def test_real(self):
    #     d = DlnaDevices("d_test_cache")
    #     devices = d.get_devices()
    #
    #     for location, device in devices.items():
    #         print str(device) + "   - " + device.info['deviceType']
    #         # print device.info
    #         print ""
    #
    #     # print d.get_device_by_type("urn:schemas-upnp-org:device:MediaRenderer:1")
    #     device = d.get_device_by_type("urn:dial-multiscreen-org:device:dialreceiver:1")
    #     print device
    #     print device.applicationUrl
