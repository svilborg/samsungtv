import logging
import os

logger = logging.getLogger(__name__)


class HttpProxyServerCtrl(object):

    def __init__(self, host="", port=8000, pid_file=""):
        """
        Httpd Control
        :type port: int
        :type host: str
        """

        dir_path = os.path.dirname(os.path.realpath(__file__))

        self.host = host
        self.port = port
        self.pid_file = pid_file if pid_file is not "" else "./stvpid"
        self.server = "{0}/server.py".format(dir_path)

        logger.info('pid {}'.format(self.pid_file))
        logger.info('server {}'.format(self.server))

        # self.logging.info("Test")

    def stop(self):
        if os.path.isfile(self.pid_file):
            cmd = "cat {} | xargs kill && rm {}".format(self.pid_file, self.pid_file)
            os.system(cmd)

        pass

    def start(self):
        self.stop()

        server_cmd = self.server

        if self.host is not "" :
            server_cmd += " -h " + self.host

        if self.port :
            server_cmd += " -p " + str(self.port)

        cmd = "nohup python {} & echo $! > {}".format(server_cmd, self.pid_file)

        os.system(cmd)

        logger.debug('cmd {}'.format(cmd))
        logger.info("Http Server Started @ {0}:{1}".format(self.host, str(self.port)))

    def get_pid(self):
        pid = ""

        if os.path.isfile(self.pid_file):
            with open(self.pid_file, 'r') as handle:
                pid = handle.read(1024)

            handle.close()

        return pid


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    httpdctrl = HttpProxyServerCtrl()

    httpdctrl.get_pid()
    httpdctrl.start()
    print httpdctrl.get_pid()
    httpdctrl.stop()
