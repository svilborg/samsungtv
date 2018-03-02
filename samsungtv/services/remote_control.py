import json
import time
import base64
import websocket


class RemoteControl():
    URL = "ws://{}:{}/api/v2/channels/samsung.remote.control?name={}"

    KEY_CODES = [
        "KEY_POWEROFF", "KEY_UP", "KEY_DOWN", "KEY_LEFT", "KEY_RIGHT", "KEY_CHUP", "KEY_CHDOWN", "KEY_ENTER",
        "KEY_RETURN", "KEY_EXIT", "KEY_CONTENTS", "KEY_CH_LIST", "KEY_MENU", "KEY_SOURCE", "KEY_GUIDE", "KEY_TOOLS",
        "KEY_INFO", "KEY_RED", "KEY_GREEN", "KEY_YELLOW", "KEY_BLUE", "KEY_PANNEL_CHDOWN", "KEY_VOLUP",
        "KEY_VOLDOWN", "KEY_MUTE",
        "KEY_DTV", "KEY_HDMI",
        "KEY_0", "KEY_1", "KEY_2", "KEY_3", "KEY_4", "KEY_5", "KEY_6", "KEY_7", "KEY_8",
        "KEY_9",
    ]

    def __init__(self, host, port=8001, name=u'RemoteControl', timeout=20, key_delay=1):

        self.id = None

        self.name = name
        self.host = host
        self.port = port
        self.timeout = timeout
        self.connection = None
        self.key_delay = key_delay

    def connect(self):

        url = RemoteControl.URL.format(self.host, self.port, self._encode(self.name))

        self.connection = websocket.create_connection(url, self.timeout)

        response = self._receive()

        if response.get("data") is None or response.get("event") != "ms.channel.connect":
            self.close()

        self.id = response["data"]["id"]

        return self.id

    def close(self):
        if self.is_connected():
            self.connection.close()

    def is_connected(self):

        if self.connection and self.connection.connected is True:
            return True

        return False

    def test(self, d):

        msg = {
            "method": "ms.channel.emit",
            "params": {
                "event": "ed.apps.search",
                # "event": "seek",
                "data": 100,
                "to": "host"
            }
        }

        response = self._send_and_receive(msg)
        return response

    def apps(self):

        msg = {
            "method": "ms.channel.emit",
            "params": {
                "event": "ed.installedApp.get",
                "to": "host"
            }}

        response = self._send_and_receive(msg)

        return response['data']['data']

    def launch(self, app_id=""):

        msg = {
            "method": "ms.channel.emit",
            "params": {
                "event": "ed.apps.launch",
                "to": "host",
                "data": {
                    "appId": app_id,
                    "action_type": "NATIVE_LAUNCH"
                }
            }}

        response = self._send_and_receive(msg)
        time.sleep(self.key_delay)

        return response

    def command(self, key_code):

        msg = {
            "method": "ms.remote.control",
            "params": {
                "Cmd": "Click",
                "DataOfCmd": key_code,
                "Option": "false",
                "TypeOfRemote": "SendRemoteKey"
            }
        }

        result = self._send(msg)

        time.sleep(self.key_delay)

        return result

    def _send(self, msg):
        if not self.is_connected():
            raise Exception("No Websocket Connection")

        data = json.dumps(msg)

        return self.connection.send(data)

    def _receive(self):
        response = self.connection.recv()

        response = json.loads(response)
        return response

    def _send_and_receive(self, msg):

        self._send(msg)

        response = self._receive()

        return response

    def _encode(self, input):
        if type(input) != unicode:
            input = input.decode('utf-8')

        return base64.b64encode(input).decode("utf-8")
