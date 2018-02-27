import getopt
import sys
import time

from dlna import DlnaDevices, DialService, utils
from upnpservice import UPnPServiceAVTransport, UPnPServiceRendering
from httpd import HttpProxyServerCtrl

VERSION = "1.0"


class SamsungTVAction(object):

    def __init__(self, label, result=None):
        self.label = label
        self.result = result
        pass

    def __repr__(self):
        return self.label


class SamsungTVActionList(object):

    def __init__(self, label, result=None, fields=[]):
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

        devices = DlnaDevices("devices")

        tv_device = devices.get_device_by_type("urn:schemas-upnp-org:device:MediaRenderer:1")
        dial_device = devices.get_device_by_type("urn:dial-multiscreen-org:device:dialreceiver:1")

        if not tv_device:
            print "Unable to find a tv device in local network"
            devices.clean()  # Cleanup if cache
            exit(1)

        if not dial_device:
            print "Unable to find a ttv dial device in local network"
            devices.clean()  # Cleanup if cache
            exit(1)

        self.app_ip = utils.detect_ip_address()
        self.volume_step = 2

        self.service = UPnPServiceAVTransport(tv_device.ip)
        self.service_rendering = UPnPServiceRendering(tv_device.ip)
        self.service_dial = DialService(dial_device.applicationUrl)
        self.httpctrl = HttpProxyServerCtrl(port=8000)

        pass

    @staticmethod
    def scan(rescan=False):

        print "Scanning ..."

        devices = DlnaDevices("devices")

        for key, device in devices.get_devices(rescan).items():
            print device
            # pprint.pprint( device.info)
            pass

    def stop_httpd(self, args=None):

        self.httpctrl.stop()
        return "Http Server Stopped"

    def start_httpd(self, args=None):
        self.httpctrl.start()

        print "Http Server Started"

    def file(self, arg):
        self.start_httpd()

        time.sleep(2)

        url = arg
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
            self.service_rendering.volume(vol)
        )

    def voldown(self, arg):
        vol = str(self.service_rendering.volume() - self.volume_step)

        return SamsungTVAction(
            "Decr Volime to %s" % (vol),
            self.service_rendering.volume(vol)
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

    def app_on(self, arg):
        return SamsungTVAction(
            "Start App %s " % (arg),
            self.service_dial.start(arg)
        )

    def app_off(self, arg):
        return SamsungTVAction(
            "Stop App %s " % (arg),
            self.service_dial.stop(arg)
        )

    def app(self, arg):
        print "App %s " % (arg)
        print self.service_dial.get(arg)
        return ""

    def app_install(self, arg):
        return SamsungTVAction(
            "Install App %s " % (arg),
            self.service_dial.install(arg)
        )

    def run(self, method, arg):
        return self.__getattribute__(method)(arg)


def usage_option(name, description):
    return "\t--%s     \t %s" % (name, description)


def usage():
    print ""
    print "Usage: " + sys.argv[0] + " [OPTIONS]"
    print usage_option("scan", "SSPD Scan")
    print usage_option("volume", "Set Volume")
    print usage_option("volup", "Incr Volume")
    print usage_option("voldown", "Decr Volume")
    print usage_option("help", "This help menu")
    print usage_option("start_httpd", "Start http server")
    print usage_option("stop_httpd", "Stop http server")
    print ""


if __name__ == "__main__":

    try:
        opts, args = getopt.getopt(sys.argv[1:], "s:hv", ["help", "version",
                                                          "scan", "rescan",
                                                          "volume=", "volup", "voldown", "mute", "unmute",
                                                          "file=",
                                                          "add_file=",
                                                          "play", "stop", "next", "prev",
                                                          "start_httpd", "stop_httpd",

                                                          "app=", "app_on=", "app_off=", "app_install="
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
        elif o in ("-s", "--scan"):
            SamsungTvApp.scan()
        elif o in ("--rescan"):
            SamsungTvApp.scan(True)
        else:
            tv = SamsungTvApp()

            method = o.replace("--", "")
            print tv.run(method, arg)
