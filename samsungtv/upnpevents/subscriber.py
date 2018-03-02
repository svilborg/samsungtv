import requests


class EventSubscriber:

    def __init__(self, url="", callback=""):

        self.url = url
        self.callback = callback
        pass

    def subscribe(self, timeout=1000):
        headers = {
            u'TIMEOUT': '5000',
            u'NT': 'upnp:event',
            u'CALLBACK': '<{}/>'.format(self.callback),
            u'User-Agent': 'HTTPSamsungCtrlCli'
        }

        result = {}

        response = requests.request(method='subscribe',
                                    url=self.url,
                                    headers=headers,
                                    verify=True,
                                    stream=True,
                                    timeout=30,
                                    allow_redirects=False,
                                    auth=None,
                                    cert=None
                                    )

        if response.status_code == 200:
            result['date'] = response.headers['date']
            result['sid'] = response.headers['sid']
        else:
            raise Exception('Error', response.status_code)

        return result

    def renew(self, sid, timeout=1000):
        headers = {
            u'TIMEOUT': str(timeout),
            u'SID': sid,
            u'User-Agent': 'HTTPSamsungCtrlCli'
        }

        result = {}

        response = requests.request(method='subscribe',
                                    url=self.url,
                                    headers=headers,
                                    verify=True,
                                    stream=True,
                                    timeout=30,
                                    allow_redirects=False,
                                    auth=None,
                                    cert=None
                                    )

        if response.status_code == 200:
            result['date'] = response.headers['date']
            result['sid'] = response.headers['sid']
        else:
            raise Exception('Error', response.status_code)

        return result

    def cancel(self, sid):
        headers = {
            'SID': sid
        }

        response = requests.request(method='UNSUBSCRIBE',
                                    url=self.url,
                                    headers=headers)
        if response.status_code == 200:
            return True
        else:
            raise Exception('Error', response.status_code)

        pass
