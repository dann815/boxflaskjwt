# coding: utf-8

from __future__ import unicode_literals
from boxsdk.network.default_network import DefaultNetwork
from pprint import pformat
from util import setup_logging


class LoggingNetwork(DefaultNetwork):
    """
    SDK Network subclass that logs requests and responses.
    """
    def __init__(self):
        super(LoggingNetwork, self).__init__()
        self._logger = setup_logging(name='network')

    def _log_request(self, method, url, **kwargs):
        """
        Logs information about the Box API request.

        :param method:
            The HTTP verb that should be used to make the request.
        :type method:
            `unicode`
        :param url:
            The URL for the request.
        :type url:
            `unicode`
        :param access_token:
            The OAuth2 access token used to authorize the request.
        :type access_token:
            `unicode`
        """
        self._logger.info('%s %s %s', method, url, pformat(kwargs))

    def _log_response(self, response):
        """
        Logs information about the Box API response.

        :param response: The Box API response.
        """
        if response.ok:
            self._logger.info(response.content)
        else:
            self._logger.warning('%s\n%s\n%s\n', response.status_code, response.headers, pformat(response.content))

    def request(self, method, url, access_token, **kwargs):
        """
        Base class override. Logs information about an API request and response in addition to making the request.
        """
        self._log_request(method, url, **kwargs)
        response = super(LoggingNetwork, self).request(method, url, access_token, **kwargs)
        self._log_response(response)
        return response