import asyncio
import websockets
import json
import ssl
import certifi

ssl_context = ssl.create_default_context(cafile=certifi.where())
_default_ping_delay_seconds = 5


class ClientBase:
    """
    Base class for communicating with trade engine websockets interfaces.

    Attributes:
        _on_message (func(str)): Function called when a new message arrives, must be able to handle a json string.
        _ws_url (str): Url to websockets interface of trade engine.
        _on_error (func(Exception)): Function called when an error happens during normal operation, must be able to
                                     handle an exception object.
    """
    def __init__(self, on_message, ws_url, on_error=None):
        """
        Args:
            on_message (func(str), required): Function called when a new message arrives, must be able to handle a json
                                              string.
            ws_url (str, required): Url to websockets interface of trade engine.
            on_error (func(Exception), optional): Function called when an error happens during normal operation, must be
                                                  able to handle an exception object.
        """
        self._on_message = on_message
        self._ws_url = ws_url
        self._on_error = on_error
        self._websocket = None
        self._conn_event = None
        self._ping_task = None
        self._keep_alive = False
        self._conn_task = None
        self._ping_delay_seconds = _default_ping_delay_seconds

    async def connect(self):
        """
        Starts an async connection and maintains pings to the server so the connection stays established.
        """
        if self._websocket is not None:
            raise RuntimeError('Already connected to websocket')

        self._conn_event = asyncio.Event()
        self._keep_alive = True
        self._conn_task = asyncio.create_task(self._connect())
        self._ping_task = asyncio.create_task(self._ping())

        try:
            await asyncio.wait_for(self._conn_event.wait(), timeout=60)
        except asyncio.TimeoutError:
            self._keep_alive = False

            await self._cancel_ping_task()
            await self._cancel_conn_task()
            self._conn_event = None

            raise RuntimeError('Failed to connect to websocket')

    async def disconnect(self):
        """
        Disconnects from the websocket connection to the server and stops sending pings.
        """
        if self._websocket is None:
            raise RuntimeError('Not connected to websocket')

        self._keep_alive = False

        await self._cancel_ping_task()
        await self._cancel_conn_task()
        self._conn_event = None

    async def _connect(self):
        """
        Internal connection task, monitors connection for new messages and reconnects if necessary.  New messages are
        sent to the _on_message attribute and errors are sent to the _on_error attribute.
        """
        while self._keep_alive:
            try:
                async with websockets.connect(self._ws_url, ssl=ssl_context) as socket:
                    self._websocket = socket
                    self._conn_event.set()

                    while self._keep_alive:
                        try:
                            msg = await socket.recv()
                            msg = json.loads(msg)
                            self._on_message(msg)
                        except Exception as err:
                            if self._on_error is not None:
                                self._on_error(err)
            except Exception as err:
                if self._on_error is not None:
                    self._on_error(err)
                # sleep before reconnecting
                await asyncio.sleep(1)
                continue
            finally:
                self._websocket = None
                self._conn_event.clear()

    async def subscribe(self, channels, symbols=None, **kwargs):
        """
        Subscribe to a channel or set of channels for single or many instruments, must call connect() first. Please
        refer to [websocket docs](https://docs.poloniex.com/#notes) for valid channels, symbols and arguments.

        Args:
            channels (str[]): List of channels for subscription command.
            symbols (str[]): List of symbols for subscription command.

        Keyword Args:
            Dictionary of any additional parameters for the subscription request.

        Returns:
            _on_message callback function will be called with response messages.
        """
        msg = {
            'event': 'subscribe',
            'channel': channels
        }

        if symbols is not None:
            msg.update({'symbols': symbols})

        msg.update(kwargs)

        await self._send_message(msg)

    async def unsubscribe(self, channels, symbols=None):
        """
        Unsubscribe from a channel or set of channels for single or many instruments.

        Args:
            channels (str[]): List of channels for unsubscribe command.
            symbols (str[]): List of symbols for unsubscribe command.

        Returns:
            _on_message callback function will be called with response messages.
        """
        msg = {
            'event': 'unsubscribe',
            'channel': channels
        }

        if symbols is not None:
            msg.update({'symbols': symbols})
        await self._send_message(msg)

    async def unsubscribe_all(self):
        """
        Unsubscribes from all current subscriptions.

        Returns:
            _on_message callback function will be called with response messages.
        """
        msg = {'event': 'unsubscribe_all'}
        await self._send_message(msg)

    async def list_subscriptions(self):
        """
        Lists all current subscriptions.

        Returns:
            _on_message callback function will be called with response messages.
        """
        msg = {'event': 'list_subscriptions'}
        await self._send_message(msg)

    async def _cancel_conn_task(self):
        """
        Internal function to cancel connection task.
        """
        self._conn_task.cancel()

        try:
            await self._conn_task
        except asyncio.CancelledError:
            pass

        self._conn_task = None

    async def _send_message(self, msg):
        """
        Internal send message function converts to json and sends to the websocket connection.

        Args:
            msg(dict): Dictionary of message parameters.
        """
        if self._websocket is None:
            raise RuntimeError('Not connected to websocket')

        msg = json.dumps(msg)
        await self._websocket.send(msg)

    async def _ping(self):
        """
        Main ping task function, sends a ping to the server every 10 seconds.  If the server does not receive a ping at
        least every 30 seconds from the client it auto disconnects.
        """
        while self._keep_alive:
            await self._conn_event.wait()

            msg = {'event': 'ping'}
            await self._send_message(msg)

            await asyncio.sleep(self._ping_delay_seconds)

    async def _cancel_ping_task(self):
        """
        Internal function to cancel ping task.
        """
        self._ping_task.cancel()

        try:
            await self._ping_task
        except asyncio.CancelledError:
            pass

        self._ping_task = None
