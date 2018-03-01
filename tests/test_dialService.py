import requests
from unittest import TestCase

# from mock import MagicMock
import mock

# from dlna import DialService
from samsungtv.dlna import DialService


def mock_response(status=200, content=""):
    resp = mock.Mock()

    resp.status_code = status
    resp.content = content

    # resp.json = mock.Mock(
    #     return_value=json_data
    # )
    return resp


# requests.get = mock.MagicMock(side_effect=mock_response)
requests.post = mock.MagicMock(side_effect=mock_response)

class TestDialService(TestCase):

    @mock.patch('requests.post')
    def test_start(self, mock_post):

        mock_post.return_value = mock_response(200, "TEST")

        service = DialService("httrp://fake.me/test")
        result = service.start("Netflix")

        print result
        self.assertEquals(result, "TEST")
        # self.fail()
