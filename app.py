import getopt
import sys
import time
import os
from dlna_device import DlnaDevice
from ssdp import SSDPDiscovery
from utils import detect_ip_address
# from upnpservice_rendering import UPnPServiceRendering
# from upnpservice_avtransport import UPnPServiceAVTransport
# from upnpservice import upnpservice_avtransport

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
        self.ip = detect_ip_address()
        self.service = UPnPServiceAVTransport('192.168.0.100')
        self.service_rendering = UPnPServiceRendering('192.168.0.100')
        self.volume_step = 2
        pass

    def scan(self, arg):
        discovery = SSDPDiscovery()
        
        print "Scanning ..."

        devices = {}
        result = discovery.discover("ssdp:all")

        for headers in result:
            devices[headers['location']] = DlnaDevice(headers['location'])
            print devices[headers['location']]

    def stop_httpd(self, args=None):
        
        if os.path.isfile("./stvpid") :
            os.system("cat ./stvpid | xargs kill && rm ./stvpid")

        return None
        
    def start_httpd(self, host = "", port = 8000):
        self.stop_httpd()
        os.system("nohup python ./serve.py & echo $! > ./stvpid")

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