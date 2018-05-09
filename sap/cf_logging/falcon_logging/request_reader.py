""" Falcon request reader """

import base64
import binascii
import logging

from sap.cf_logging import defaults
from sap.cf_logging.core.request_reader import RequestReader


class FalconRequestReader(RequestReader):
    def get_remote_user(self, request):
        remote_user = defaults.UNKNOWN
        http_auth = request.get_header('Authorization')
        if http_auth and http_auth.startswith('Basic'):
            auth_parts = http_auth.split(' ', 1)
            if len(auth_parts) == 2:
                try:
                    tokens = base64.b64decode(
                        auth_parts[1].strip().encode('utf-8')).decode('utf-8')
                    tokens = tokens.split(":", 1)
                except (TypeError, binascii.Error, UnicodeDecodeError) as exc:
                    logging.debug("Couldn't get username: %s", exc)
                    return remote_user
                if len(tokens) == 2:
                    remote_user = tokens[0]
        return remote_user

    def get_protocol(self, request):
        return request.scheme

    def get_content_length(self, request):
        return request.content_length

    def get_remote_ip(self, request):
        return request.remote_addr

    def get_remote_port(self, request):
        return defaults.UNKNOWN
