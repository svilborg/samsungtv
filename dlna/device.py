
import xml.etree.cElementTree as XML
import requests
# import pprint
import re
import urlparse
from utils import etree_to_dict


class DlnaDevice(object):

    def __init__(self, location = ""):
   
      parsed = urlparse.urlparse(location)

      self.ip = parsed.hostname
      self.port = parsed.port
      self.path = parsed.path
      self.location = location

      data = self.__get_data(location)
      
      self.info = data['root']['device']
      self.name = self.info['friendlyName']
      self.services = data['root']['device']['serviceList']['service']      

      # pprint.pprint(self.services)

    def __get_data(self, location):
        r = requests.get(location)

        xmlstring = r.content
        xmlstring = re.sub(' xmlns="[^"]+"', '', xmlstring, count=1)

        xml = XML.fromstring(xmlstring)
        data = etree_to_dict(xml)
        return data

    def __repr__(self):
        
        res = ""
        res += self.name + "  [ " + self.info["modelName"] + ", " + self.info["modelDescription"] + " ] @  " + self.location + "\n"
 
        return res

if __name__ == "__main__":
    print "DlnaDevice"
    # d = DlnaDevice("http://192.168.0.1:49152/wps_device.xml")