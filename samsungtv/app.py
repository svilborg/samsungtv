import time

from httpd import HttpProxyServerCtrl
from dlna import DlnaDevices, utils, DlnaDeviceServices
from samsungtv.services.remote_control import RemoteControl

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

            if isinstance(item, dict):
                for field in self.fields:
                    res += item[field] + "  "
                    pass
            elif isinstance(item, str):
                res += item
            else:
                raise Exception("Unknown item type {}".format(type(item)))

            res += "\n"

        return res


class SamsungTvApp(object):
    """docstring for SamsungTvApp"""

    def __init__(self):

        self.host = utils.detect_ip_address()
        self.port = 8000
        self.name = u'SamsungTvApp'
        self.uri = "http://" + self.host + ":" + str(self.port)
        self.app_ip = utils.detect_ip_address()
        self.volume_step = 2

        devices = DlnaDevices("devices")

        tv_device = devices.get_device_by_type(DlnaDevices.MEDIA_RENDERER)
        dial_device = devices.get_device_by_type(DlnaDevices.DIAL_RECEIVER)

        if not tv_device:
            print "Unable to find a tv device in local network"
            devices.clean()  # Cleanup if cache
            exit(1)

        if not dial_device:
            print "Unable to find a ttv dial device in local network"
            devices.clean()  # Cleanup if cache
            exit(1)

        # c = DlnaDeviceServices.subscribe_to_all(tv_device, self.uri)
        # print c
        # exit(1)

        self.service = DlnaDeviceServices.get_service(tv_device, DlnaDeviceServices.SERVICE_AV)
        self.service_rendering = DlnaDeviceServices.get_service(tv_device, DlnaDeviceServices.SERVICE_RC)
        self.service_dial = DlnaDeviceServices.get_service(dial_device, DlnaDeviceServices.SERVICE_DIAL)
        self.remote_control = RemoteControl("192.168.0.100", name=self.name)

        self.httpctrl = HttpProxyServerCtrl(port=self.port)

        pass

    @staticmethod
    def scan(rescan=False):

        print "Scanning ..."

        devices = DlnaDevices("devices")

        for key, device in devices.get_devices(rescan).items():
            print device
            # import pprint
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
        print url
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

    def keys(self, arg):

        return SamsungTVActionList(
            "Keys \n",
            RemoteControl.KEY_CODES
        )

    def key(self, arg):
        """

        :type arg: str
        """

        if arg.find(",") > 0:
            key_codes = arg.split(",")

            self.remote_control.connect()
            for key_code in key_codes:
                # self.key(key_code)
                self.remote_control.command(key_code)
            self.remote_control.close()

            return SamsungTVAction(
                "Keys Pressed \n " +
                "\n ".join(key_codes)
            )
        else:
            self.remote_control.connect()
            result = self.remote_control.command(arg)
            self.remote_control.close()

            return SamsungTVAction(
                "Key Pressed %s" % arg,
                result
            )

    def launch(self, arg):

        self.remote_control.connect()
        result = self.remote_control.launch(arg)
        self.remote_control.close()

        return SamsungTVAction(
            "App Launched %s" % arg,
            result
        )

    def apps(self, arg=None):

        self.remote_control.connect()
        app_list = self.remote_control.apps()
        self.remote_control.close()

        return SamsungTVActionList("Apps \n", app_list, ["appId", "name"])

    def run(self, method, arg):
        return self.__getattribute__(method)(arg)
