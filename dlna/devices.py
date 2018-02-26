
from utils import Cache
from ssdp import SSDPDiscovery
from device import DlnaDevice

class DlnaDevices(object):

    def __init__(self, cache = None):
        self.cache = cache

        pass

    def _get_devices(self) :
        discovery = SSDPDiscovery()
        result = discovery.discover("ssdp:all")
        devices = {}

        for headers in result:
            devices[headers['location']] = DlnaDevice(headers['location'])

        return devices

    def get_devices(self, refresh = False):
        devices = {}

        if self.cache :
            if refresh == True or not Cache.get(self.cache):
                devices = self._get_devices()

                Cache.set(self.cache, devices)
            else :
                devices = Cache.get(self.cache)
        else :
            devices = self._get_devices()

        return devices

    def get_device_by_type(self, type = ""):

        for key,device in self.get_devices().items():
            if device.info['deviceType'] == "urn:schemas-upnp-org:device:MediaRenderer:1" :
                return device
        return None

    def clean(self) :
        if self.cache :
            Cache.clear(self.cache)

if __name__ == "__main__":

    print "DlnaDevices"

    d = DlnaDevices("d_test_cache")
    devices = d.get_devices()

    for location, device in devices.items() :
        print str(device) + "   - " + device.info['deviceType']
        print ""

    print "============"
    print d.get_device_by_type("urn:schemas-upnp-org:device:MediaRenderer:1")

