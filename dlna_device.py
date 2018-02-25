
import xml.etree.cElementTree as XML
import requests
import pprint
import re
import urlparse
from collections import defaultdict

def etree_to_dict(t):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k:v[0] if len(v) == 1 else v for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v) for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
              d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d

class DlnaDevice(object):

    def __init__(self, location = ""):
   
      parsed = urlparse.urlparse(location)

      self.ip = parsed.hostname
      self.port = parsed.port
      self.path = parsed.path
      self.location = location

      data = self.get_data(location)
      
      self.device_data = data['root']['device']
      self.services = data['root']['device']['serviceList']['service']      
      self.name = self.device_data['friendlyName']

      # print self.ip
      # print self.port
      # print self.path
      # print self.location
      pprint.pprint(self.services)

    def get_data(self, location):
        r = requests.get(location)

        xmlstring = r.content
        xmlstring = re.sub(' xmlns="[^"]+"', '', xmlstring, count=1)

        xml = XML.fromstring(xmlstring)
        data = etree_to_dict(xml)
        return data

    def __repr__(self):
        
        res = ""
        res += self.name + "  [ " + self.device_data["modelName"] + ", " + self.device_data["modelDescription"] + " ] @  " + self.location + "\n"
 
        return res

if __name__ == "__main__":
    print "DlnaDevice"
    # d = DlnaDevice("http://192.168.0.1:49152/wps_device.xml")