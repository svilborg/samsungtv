class DlnaDeviceServices:
    SERVICE_AV = "urn:schemas-upnp-org:service:AVTransport:1"
    SERVICE_RC = "urn:schemas-upnp-org:service:RenderingControl:1"
    SERVICE_CM = "urn:schemas-upnp-org:service:ConnectionManager:1"
    SERVICE_DIAL = "dial"

    @staticmethod
    def get_service(device, type):

        if device.services.get(type) is None and type is not DlnaDeviceServices.SERVICE_DIAL:
            raise Exception("Unsupported service {}".format(type))

        if type == DlnaDeviceServices.SERVICE_AV:
            from upnpservice import UPnPServiceAVTransport

            return UPnPServiceAVTransport(device.ip, device.port, config=device.services[type])

        elif type == DlnaDeviceServices.SERVICE_RC:

            from upnpservice import UPnPServiceRendering

            return UPnPServiceRendering(device.ip, device.port, config=device.services[type])
        elif type == DlnaDeviceServices.SERVICE_CM:
            from upnpservice import UPnPServiceConnectionManager

            return UPnPServiceConnectionManager(device.ip, device.port, config=device.services[type])
        elif type == DlnaDeviceServices.SERVICE_DIAL:

            if device.applicationUrl is not None and device.applicationUrl != "":
                from dlna import DialService
                return DialService(device.applicationUrl)
            else:
                raise Exception("Device  does not support service ()".format(type))

        else:
            raise Exception("Unsupported service ()".format(type))

    @staticmethod
    def get_event_subscriber(device, type, callback=""):

        if device.services.get(type):
            url = "http://{}:{}{}".format(device.ip, device.port, device.services[type]['eventSubURL'])

            print "========"
            print device.services[type]
            print url

            from upnpevents import EventSubscriber

            return EventSubscriber(url, callback)

        else:
            raise Exception("Unsupported event service ()".format(type))

        pass

    @staticmethod
    def get_event_subscribers(device, callback=""):

        subscribers = {}

        print device.info

        for stype, service in device.services.items():
            if service.get('eventSubURL'):
                subscribers[stype] = DlnaDeviceServices.get_event_subscriber(device, stype, callback)

        return subscribers

    @staticmethod
    def subscribe(device, type, callback=""):
        subscriber = DlnaDeviceServices.get_event_subscriber(device, type, callback)
        subscriber.subscribe()

    @staticmethod
    def subscribe_to_all(device, callback=""):

        for stype, subscriber in DlnaDeviceServices.get_event_subscribers(device, callback).items():
            print subscriber
            subscriber.subscribe()
