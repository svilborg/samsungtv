import socket


class SSDPDiscovery(object):
    ip = "239.255.255.250"
    port = 1900

    ST_ALL = "ssdp:all"
    ST_ROOT = "upnp:rootdevice"

    def discover(self, service, timeout=10.0, retries=3, mx=3):

        message = "\r\n".join([
            'M-SEARCH * HTTP/1.1',
            'HOST: {0.ip}:{0.port}',
            'Accept: */*',
            'MAN: "ssdp:discover"',
            'ST: {st}',
            'MX: {mx}', '', ''])

        message = message.format(self, st=service, mx=mx)

        socket.setdefaulttimeout(timeout)
        responses = {}

        for _ in range(retries):

            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
            sock.sendto(message, (self.ip, self.port))

            while True:
                try:
                    response = self._get_response(sock.recvfrom(1024))
                    responses[response['location']] = response

                except socket.timeout:
                    break

        return responses.values()

    def _get_response(self, response):
        headers, addr = response

        result = {
            'ip': addr[0],
            'port': addr[1]
        }

        for s in headers.splitlines():
            x = s.split(": ")
            if len(x) == 2:
                result[x[0].lower()] = x[1]
        return result
