import json

import mock
from unittest import TestCase
from samsungtv.services.remote_control import RemoteControl
from tests.mocks import mock_ws_conn


class TestRemoteControl(TestCase):

    def setUp(self):
        self.rc = RemoteControl("192.168.0.100")

    @mock.patch('samsungtv.services.remote_control.websocket')
    def test_connect(self, mock_ws):
        mock_ws.create_connection.return_value = mock_ws_conn({'data': {'id': 'ID_OK'}})

        id = self.rc.connect()
        self.rc.close()

        self.assertIsNotNone(id)
        self.assertEquals(id, u'ID_OK')

    @mock.patch('samsungtv.services.remote_control.websocket')
    def test_command(self, mock_ws):
        mock_ws.create_connection.return_value = mock_ws_conn({'data': {'id': 'ID_OK'}})

        id = self.rc.connect()
        r = self.rc.command("KEY_2")
        self.rc.close()

        self.assertIsNotNone(id)

    @mock.patch('samsungtv.services.remote_control.websocket')
    def test_launch(self, mock_ws):
        mock_ws.create_connection.return_value = mock_ws_conn({'data': {'id': 'ID_OK'}})
        id = self.rc.connect()
        r = self.rc.launch("org.tizen.browser")

        self.rc.close()

# def test_real(self):
# rc = RemoteControl("192.168.0.100")
# rc.connect()
# rc.command("KEY_0")
# print rc.test("com.tizen.browser")
# print rc.apps()
# print rc.launch(20162100002)
# print rc.launch("org.tizen.browser")
# rc.launch("com.netflix.samsung")
# rc.launch("com.netflix.tizen")
# rc.close()
