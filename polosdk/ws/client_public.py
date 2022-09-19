from polosdk.ws.client_base import ClientBase
from urllib.parse import urljoin

_default_ws_url = 'wss://ws.poloniex.com/ws/'

class ClientPublic(ClientBase):
    """
    Websockets client for public connections. See [public channel](https://docs.poloniex.com/#public-channels)
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
        ClientBase.__init__(self, on_message, urljoin(ws_url_base, 'public'), on_error)
