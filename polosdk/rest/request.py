import json
import urllib

import requests
import base64
import hashlib
import hmac
from datetime import datetime
from urllib.parse import urljoin


_default_url = 'https://api.poloniex.com'


class RequestError(Exception):
    """
    Exception class used to report errors from trade engine.

    Attributes:
        code (int): Error code reported from trade engine.
        message (str): Associated message.
    """
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f'code: {self.code}, message: {self.message}'


def encode_uri_component(component):
    return urllib.parse.quote(str(component), safe='~()*!\'')


class Request:
    """
    Creates, authenticates and handles responses from trade engine.

    Attributes:
         _api_key (str): User api key used for authentication.
         _api_secret (str): User api key used for authentication.
         _url (str): Url used for communicating with server.
         _timeout_sec (int): Timeout for REST connections.
    """
    def __init__(self, api_key=None, api_secret=None, url=None, timeout_sec=5):
        """
        Args:
            api_key (str, required): User api key used for authentication.
            api_secret (str, required): User api key used for authentication.
            url (str, optional): Url used for communicating with server. Default Production url.
            timeout_sec (int, optional): Timeout for REST connections. Default 5 seconds.
        """
        self._api_key = api_key
        self._api_secret = api_secret.encode('utf8') if api_secret is not None else None
        self._url = url or _default_url
        self._timeout_sec = timeout_sec

    def __call__(self, method, path, auth=False, params={}, body={}):
        """
        Executes a server request.

        Args:
            method (str, required): Method for request e.g. GET, POST, PUT, DELETE.
            path (str, required): Endpoint path that is added to base url e.g. /accounts, /markets.
            auth (bool, optional): Where or not this call requires authentication.
            params (dict, optional): Dictionary of parameters to be passed as arguments in the url.
            body (dict, optional): Dictionary of parameters to be passed as arguments in the body.

        Returns:
            Json object with server response.

        Raises:
            RequestError: An error occurred communicating with trade engine.
            RuntimeError: An error occurred parsing the response from the server.
        """
        headers = {}
        method = method.upper()

        if len(body) > 0:
            headers.update({'content-type': 'application/json'})
            body = json.dumps(body)

        if auth:
            if self._api_secret is not None and self._api_key is not None:
                headers.update(self._get_sig_header(method, path, params, body))
            else:
                raise RequestError(-1, "Authenticated endpoints required api_secret and api_key to be set.")

        url = urljoin(self._url, path)
        response = requests.request(method,
                                    url,
                                    headers=headers,
                                    timeout=self._timeout_sec,
                                    params=params,
                                    data=body)
        try:
            response_json = response.json()
        except Exception:
            if response.status_code != 200:
                response.raise_for_status()

            raise RuntimeError(response.text)

        if response.status_code != 200:
            raise RequestError(response_json.get('code', None),
                               response_json.get('message', response.text))

        return response_json

    def _get_sig_header(self, method, path, params, body):
        """
        Creates signature headers needed for an authed request.

        Args:
            method (str, required): Method for request e.g. GET, POST, PUT, DELETE.
            path (str, required): Endpoint path that is added to base url e.g. /accounts, /markets.
            params (dict, optional): Dictionary of parameters to be passed as arguments in the url.  Used to generate
                                     signature.
            body (json, optional): Json object of parameters to be passed as arguments in the body.  Used to generate
                                   signature.

        Returns:
            Json object with server response.
        """
        timestamp = str(int(datetime.now().timestamp() * 1000))

        if len(body) == 0:
            params_internal = {'signTimestamp': timestamp}
            params_internal.update(params)
            params_auth = [f'{key}={encode_uri_component(value)}' for key, value in sorted(params_internal.items())]
            params_auth = '&'.join(params_auth)
        else:
            params_auth = f'requestBody={body}&signTimestamp={timestamp}'

        payload = f'{method}\n{path}\n{params_auth}'
        sig_hash = hmac.new(self._api_secret, payload.encode('utf8'), hashlib.sha256).digest()
        signature = base64.b64encode(sig_hash).decode()

        return {
            'key': self._api_key,
            'signature': signature,
            'signTimestamp': timestamp
        }
