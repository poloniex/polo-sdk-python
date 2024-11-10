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
        Args:初始化 ClientBase 类的实例。
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
        """初始化 ClientBase 类的实例。

检查当前是否已经连接，如果是则抛出错误。

创建连接事件和保持连接的任务。

等待连接成功的事件，如果超时则抛出连接失败的错误。
        Starts an async connection and maintains pings to the server so the connection stays established.
        """
        if self._websocket is not None:
            raise RuntimeError('Already connected to websocket')

        self._conn_event = asyncio.Event()
        self._keep_alive = True
        self._conn_task = asyncio.create_task(self.listen())
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
        """断开与 WebSocket 服务器的连接。
        Disconnects from the websocket connection to the server and stops sending pings.
        """
        if self._websocket is None:
            raise RuntimeError('Not connected to websocket')

        self._keep_alive = False

        await self._cancel_ping_task()
        await self._cancel_conn_task()

        # 发送关闭帧
        try:
            await self._websocket.close()  # 确保发送关闭帧
        except Exception as e:
            print("Error while closing websocket:", e)
        self._conn_event = None

    async def listen(self):
        """
        内部连接任务，监视新消息并处理重连。
        在保持连接的状态下，使用 websockets 库连接到指定的 WebSocket URL。

在连接成功后，持续接收消息并将其传递给消息处理函数。

处理可能发生的错误，并在错误发生时执行重连逻辑。

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
                # Ensure the websocket is closed properly
                if self._websocket is not None:
                    await self._websocket.close()  # Close the websocket
                self._websocket = None
                self._conn_event.clear()

    async def subscribe(self, channels, symbols=None, **kwargs):
        """订阅一个或多个频道。
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
            # 添加其他可选参数
        msg.update(kwargs)

            # 发送消息前进行调试
        print("Sending subscribe message:", msg)  # 调试信息，查看发送的消息内容
        msg.update(kwargs)
        msg=json.dumps(msg)

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
        # print("Sending message:", msg)  # 确保格式正确
        if self._websocket is None:
            raise RuntimeError('Not connected to websocket')
        # print(f"msg的类型是{type(msg)}")
        msg = json.dumps(msg)
        # print(f"msg的类型是{type(msg)}")
        # print("Sending message:", msg)  # 确保格式正确
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
