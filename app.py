import getopt
import os
import sys
import time

from dlna import DlnaDevice, SSDPDiscovery, Cache, utils
from upnpservice import UPnPServiceAVTransport, UPnPServiceRendering


VERSION = "1.0"

class SamsungTVAction(object):

    def __init__(self, label, result=None):
        self.label = label
        self.result = result
        pass

    def __repr__(self):
        return self.label

class SamsungTVActionList(object):

    def __init__(self, label, result=None, fields = []):
        self.label = label
        self.result = result
        self.fields = fields
        
        pass

    def __repr__(self):
        
        res = "\n"
        res += self.label + "\n"
        for item in self.result:
            for field in self.fields:
                res += item[field] + "  "
                pass
            res += "\n"

        return res

class SamsungTvApp(object):
    """docstring for SamsungTvApp"""
    def __init__(self):
        
        tv_device = self._get_samsungtv()

        if not tv_device:
            print "Unable to find a tv device in local network"
            Cache.clear("devices")            
            exit(1)

        self.app_ip = utils.detect_ip_address()

        self.service = UPnPServiceAVTransport(tv_device.ip)
        self.service_rendering = UPnPServiceRendering(tv_device.ip)
        self.volume_step = 2
        pass

    def _get_samsungtv (self):

        devices = self._get_devices()

        for key,device in devices.items():
            print device

            if device.info['deviceType'] == "urn:schemas-upnp-org:device:MediaRenderer:1" :
                return device

        return None

    def _get_devices(self, refresh = False):
        discovery = SSDPDiscovery()
        devices = {}

        # dir_path = os.path.dirname(os.path.realpath(__file__))
        if refresh == True or not Cache.get("devices"):
            result = discovery.discover("ssdp:all")

            for headers in result:
                devices[headers['location']] = DlnaDevice(headers['location'])
                # print devices[headers['location']]

            Cache.set("devices", devices)
        else :
            devices = Cache.get("devices")

        return devices

    def scan(self, arg):
        
        print "Scanning ..."
        
        devices = self._get_devices()

        for key,device in devices.items():
            print device
            # pprint.pprint( device.info)
        
    def stop_httpd(self, args=None):
        
        if os.path.isfile("./stvpid") :
            os.system("cat ./stvpid | xargs kill && rm ./stvpid")

        return "Http Server Stopped"
        
    def start_httpd(self, host = "", port = 8000):
        self.stop_httpd()
        os.system("nohup python ./httpd/serve.py & echo $! > ./stvpid")

        print "Http Server Started @ " + host + ":" + str(port) 

    def file(self, arg):
       self.start_httpd()

       time.sleep(2)

       url=arg
       self.service.url(url)


    def add_file(self, arg):

        return SamsungTVAction(
            "Added URL %s" % (arg), 
            self.service.set_next_url(arg)
        )

    def play(self, arg):
        return SamsungTVAction(
            "Play %s" % (arg), 
            self.service.play()
        )

    def stop(self, arg):
        return SamsungTVAction(
            "Stop %s" % (arg), 
            self.service.stop()
        )

    def next(self, arg):
        return SamsungTVAction(
            "Next %s" % (arg), 
            self.service.next()
        )

    def prev(self, arg):
        return SamsungTVAction(
            "Stop %s" % (arg), 
            self.service.previous()
        )

    def volume(self, arg):
        return SamsungTVAction(
            "Set Volime to %s" % (arg), 
            self.service_rendering.volume(arg)
        )

    def volup(self, arg):
        vol = str(self.service_rendering.volume() + self.volume_step)

        return SamsungTVAction(
            "Incr Volime to %s" % (vol),
            self.service.volume(vol)
        )
        
    def voldown(self, arg):
        vol = str(self.service_rendering.volume() - self.volume_step)

        return SamsungTVAction(
            "Decr Volime to %s" % (vol),
            self.service.volume(vol)
        )
    
    def mute(self, arg):
        return SamsungTVAction(
            "Set Mute On",
            self.service_rendering.mute(True)
        )

    def unmute(self, arg):    
        return SamsungTVAction(
            "Set Mute Off",
            self.service_rendering.mute(False)
        )

    def run(self, method, arg):
        return self.__getattribute__(method)(arg)



def usage_option(name, description):
    return "\t--%s     \t %s"%(name, description)

def usage():
    print ""
    print "Usage: " +  sys.argv[0] + " [OPTIONS]"
    print usage_option("scan", "SSPD Scan")
    print usage_option("volume", "Set Volume")
    print usage_option("volup", "Incr Volume")
    print usage_option("voldown", "Decr Volume")
    print usage_option("help", "This help menu")
    print usage_option("start_httpd", "Start http server")
    print usage_option("stop_httpd", "Stop http server")
    print ""

if __name__ == "__main__":
    tv = SamsungTvApp()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "s:hv", ["scan", "help", "version", 
            "volume=", "volup", "voldown", "mute", "unmute", 
            "file=", 
            "add_file=", 
            "play", "stop", "next", "prev", 
            "start_httpd", "stop_httpd"
        ])
    except getopt.GetoptError, err:
        print(err)
        sys.exit(-1)

    for o, arg in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-V", "--version"):
            print VERSION
            sys.exit(0)
        else:
            method = o.replace("--", "")
            print tv.run(method, arg)