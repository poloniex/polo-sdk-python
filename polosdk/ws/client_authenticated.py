from polosdk.ws.client_base import ClientBase
from urllib.parse import urljoin
import base64
import hashlib
import hmac
from datetime import datetime

_default_ws_url = 'wss://ws.poloniex.com/ws/'


class ClientAuthenticated(ClientBase):
    """
    Websockets client for authenticated connections.  See [private channel](https://docs.poloniex.com/#authenticated-channels)
    documentation for more information on available commands.
    """
    def __init__(self, on_message, on_error=None, ws_url=None):
        """
        Args:
            on_message (func(str), required): Function called when a new message arrives, must be able to handle a json string.
            on_error (func(Exception), optional): Function called when an error happens during normal operation, must be able to
                                        handle an exception object.
            ws_url (str, optional): Url to websockets interface of trade engine. Default is to production.
        """
        ws_url_base = ws_url or _default_ws_url
        ClientBase.__init__(self, on_message, urljoin(ws_url_base, 'private'), on_error)

    async def connect(self, api_key, api_secret):
        """
        Starts an async connection and maintains pings to the server so the connection stays established.  Authenticates
        after connection.

        Args:
            api_key (str, required): User api key used for authentication.
            api_secret (str, required): User api secret used for authentication.
        """
        await super().connect()
        await self._authenticate(api_key, api_secret)

    async def _authenticate(self, api_key, api_secret):
        """
        Sends an authentication event to the server.

        Args:
            api_key (str, required): User api key used for authentication.
            api_secret (str, required): User api secret used for authentication.
        """
        ts = int(datetime.now().timestamp() * 1000)
        sign = self._get_signature(api_secret, ts)
        auth_msg = {
            'event': 'subscribe',
            'channel': ['auth'],
            'params': {
                'key': api_key,
                'signTimestamp': ts,
                'signature': sign
            }
        }
        await self._send_message(auth_msg)

    def _get_signature(self, api_secret, timestamp):
        """
        Creates the signature needed for authentication events.

        Args:
            api_secret (str, required): User api secret used for authentication.
            timestamp (int, required): Current time in ms since epoch.

        Returns:
            Generated signature as string.
        """
        payload = f'GET\n/ws\nsignTimestamp={timestamp}'
        sig_hash = hmac.new(api_secret.encode('utf8'), payload.encode('utf8'), hashlib.sha256).digest()
        secret_key = base64.b64encode(sig_hash).decode()
        return secret_key
