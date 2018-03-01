import mock


def mock_response(status=200, content=""):
    resp = mock.Mock()

    resp.status_code = status
    resp.content = content

    # resp.json = mock.Mock(
    #     return_value=json_data
    # )
    return resp
