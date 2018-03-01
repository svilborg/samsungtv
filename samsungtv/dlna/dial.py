import re
import requests
import xml.etree.cElementTree as XML


class DialService(object):

    def __init__(self, url):
        self.url = url
        pass

    def start(self, name):
        r = requests.post(self.url + name)

        return r.content

    def get(self, name):
        r = requests.get(self.url + name)

        if r.status_code == 200:
            xmlstring = r.content

            xml = XML.fromstring(xmlstring)

            ns = '{urn:dial-multiscreen-org:schemas:dial}'

            name = xml.findtext('.//' + ns + 'name')
            state = xml.findtext('.//' + ns + 'state')
            version = xml.findtext('.//' + ns + 'version')
            options = xml.find('.//' + ns + 'options')
            additional_data = xml.find('.//' + ns + 'additionalData')
            atom = xml.find('.//{http://www.w3.org/2005/Atom}link')
            install_url = None

            data = {}

            m = re.search('installable=(.*)', state)
            if m:
                state = 'installable'
                install_url = m.group(1)

            data['name'] = name
            data['state'] = state
            data['install_url'] = install_url
            data['version'] = version
            data['options'] = options.attrib if options is not None else None
            data['links'] = atom.attrib if atom is not None else None
            data['additional_data'] = {}

            if additional_data:
                for el in additional_data:
                    tag = re.sub('{[^{}]+}', '', el.tag, count=1)
                    data['additional_data'][tag] = el.text

            return data

        return None

    def install(self, name):
        app = self.get(name)

        if app['state'] == "installable" and app['install_url']:
            requests.get(app['install_url'])

    def stop(self, name):
        app = self.get(name)

        if app and app['state'] == "running":
            if app['links'] is  not None :
                requests.delete(self.url + name + "/" + app['links']['rel'])


if __name__ == "__main__":
    print "DialService"

    name = "YouTube"

    service = DialService("http://192.168.0.100:8080/ws/app/")

    print "=================="
    print service.start(name)

    print "=================="
    print service.get(name)

    print "=================="
    print service.get("Netflix")

    print "=================="
    print service.get("NetflixNope")

    print "=================="
    print service.get("uk.co.bbc.iPlayer")

    import time

    time.sleep(2)

    print "=================="
    print service.stop(name)
    # print service.install("uk.co.bbc.iPlayer")
