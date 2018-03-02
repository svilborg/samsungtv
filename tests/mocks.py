import json

import mock


def mock_response(status=200, content=""):
    resp = mock.Mock()

    resp.status_code = status
    resp.content = content

    # resp.json = mock.Mock(
    #     return_value=json_data
    # )
    return resp


def mock_ws_conn(data=None, connected=True):
    j = json.dumps(data)

    websocket_conn = mock.MagicMock()
    websocket_conn.close.return_value = True
    websocket_conn.connected = connected
    websocket_conn.recv.return_value = j

    return websocket_conn
