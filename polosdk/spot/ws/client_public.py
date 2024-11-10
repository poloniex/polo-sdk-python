import json

from polosdk.spot.ws.client_base import ClientBase
from urllib.parse import urljoin

# _default_ws_url = 'wss://ws.poloniex.com/ws/'

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
        ws_url_base = ws_url
        ClientBase.__init__(self, on_message, urljoin(ws_url_base, 'public'), on_error)


    async def subscribe_to_currencies(self):
        """订阅货币信息"""
        subscribe_message = {
            "event": "subscribe",
            "channel": ["currencies"],
            "currencies": ["ALL"]
        }
        await self._send_message(subscribe_message)


    async def subscribe_to_symbols(self):
        """订阅符号信息"""
        subscribe_message = {
            "event": "subscribe",
            "channel": ["symbols"],  # 改为字符串
            "symbols": ["btc_usdt"]
        }
        await self._send_message(subscribe_message)


    async def subscribe_to_exchange(self):
            """订阅交易信息"""
            subscribe_message = {
                "event": "subscribe",
                "channel": ["exchange" ] # 改为字符串
            }
            await self._send_message(subscribe_message)


    async def subscribe_to_candles(self):
        """订阅K线数据"""
        subscribe_message = {
            "event": "subscribe",
            "channel": ["candles_minute_1"],  # 改为字符串
            "symbols": ["BTC_USDT"]
    }
        await self._send_message(subscribe_message)


    async def subscribe_to_trades(self):
        """订阅交易信息"""
        subscribe_message = {
             "event": "subscribe",
            "channel": ["trades"],  # 改为字符串
            "symbols": ["BTC_USDT"]
        }
        await self._send_message(subscribe_message)


    async def subscribe_to_ticker(self):
        """订阅Ticker信息"""
        subscribe_message = {
            "event": "subscribe",
            "channel": ["ticker"],  # 改为字符串
            "symbols": ["btc_usdt"]
        }
        await self._send_message(subscribe_message)


    async def subscribe_to_book(self):
        """订阅市场深度"""
        subscribe_message = {
            "event": "subscribe",
            "channel": ["book"],  # 改为字符串
            "symbols": ["BTC_USDT"]
        }
        await self._send_message(subscribe_message)


    async def subscribe_to_booklv2(self):
        """订阅市场深度LV2"""
        subscribe_message = {
            "event": "subscribe",
            "channel": ["book_lv2"],  # 改为字符串
            "symbols": ["BTC_USDT"]
        }
        await self._send_message(subscribe_message)