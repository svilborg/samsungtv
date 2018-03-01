import requests
from unittest import TestCase
import mock
from tests.mocks import mock_response

from samsungtv.services.dial import DialService

requests.post = mock.MagicMock(side_effect=mock_response)


class TestDialService(TestCase):

    @mock.patch('requests.post')
    def test_start(self, mock_post):
        mock_post.return_value = mock_response(200, "TEST")

        service = DialService("httrp://fake.me/test")
        result = service.start("Netflix")

        self.assertEquals(result, "TEST")

    # @mock.patch('requests.get')
    # def test_get(self, mock_get):
    #     mock_get.return_value = mock_response(200)
    #
    #     service = DialService("httrp://fake.me/test")
    #     result = service.get("Netflix")


