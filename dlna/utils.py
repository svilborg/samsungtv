import os
import pickle
import socket
from collections import defaultdict


class Cache(object) :

    path = './cache'

    @staticmethod    
    def set(name, value):
        file = '%s/%s.pickle' % (Cache.path, name)
        
        with open(file, 'wb') as handle:
            pickle.dump(value, handle, protocol=pickle.HIGHEST_PROTOCOL)

        pass

    @staticmethod    
    def get(name):
        value = None
        file = '%s/%s.pickle' % (Cache.path, name)
        
        if os.path.isfile(file):
            with open(file, 'rb') as handle:
                value = pickle.load(handle)

        return value

    @staticmethod    
    def clear(name):
        file = '%s/%s.pickle' % (Cache.path, name)
        
        if os.path.isfile(file):
            os.remove(file)

def detect_ip_address():
    """Return the local ip-address"""
    # https://stackoverflow.com/a/166589
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address



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
