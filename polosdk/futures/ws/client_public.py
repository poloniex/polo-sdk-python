from urllib.parse import urljoin

from polosdk.futures.ws.client_base import ClientBase

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

    async def subscribe_to_ProductInfosymbol(self):

        subscribe_message = {
            "event": "subscribe",
            "channel": ["symbol"],
            "symbols": ["BTC_USDT_PERP"]
        }
        await self._send_message(subscribe_message)

    async def subscribe_to_OrderBook(self):

        subscribe_message = {
            "event": "subscribe",
            "channel": ["book"],
            "symbols": ["BTC_USDT_PERP"]
        }
        await self._send_message(subscribe_message)

    async def subscribe_to_orderbooklv2(self):

        subscribe_message = {
            "event": "subscribe",
            "channel": ["book_lv2"],
            "symbols": ["BTC_USDT_PERP"]
        }
        await self._send_message(subscribe_message)

    async def subscribe_to_KlineData(self):

        subscribe_message = {
            "event": "subscribe",
            "channel": ["candles_minute_1"],
            "symbols": ["BTC_USDT_PERP"]
        }
        await self._send_message(subscribe_message)

    async def subscribe_to_Tickers(self):

        subscribe_message = {
            "event": "subscribe",
            "channel": ["tickers"],
            "symbols": ["BTC_USDT_PERP", ""]
        }
        await self._send_message(subscribe_message)

    async def subscribe_to_Trades(self):

        subscribe_message = {
            "event": "subscribe",
            "channel": ["trades"],
            "symbols": ['BTC_USDT_PERP','BTC_USDT_PERP']
        }
        await self._send_message(subscribe_message)

    async def subscribe_to_IndexPrice(self):

        subscribe_message = {
            "event": "subscribe",
            "channel": ["index_price"],
            "symbols": ["BTC_USDT_PERP"]
        }
        await self._send_message(subscribe_message)

    async def subscribe_to_MarkPrice(self):

        subscribe_message = {
            "event": "subscribe",
            "channel": ["mark_price"],
            "symbols": ["BTC_USDT_PERP"]
        }
        await self._send_message(subscribe_message)

    async def subscribe_to_IndexPriceKlineData(self):

        subscribe_message = {
            "event": "subscribe",
            "channel": ["index_candles_minute_1"],
            "symbols": ["BTC_USDT_PERP"]
        }
        await self._send_message(subscribe_message)

    async def subscribe_to_MarkPriceKlineData(self):

        subscribe_message = {
            "event": "subscribe",
            "channel": ["mark_price_candles_minute_1"],
            "symbols": ["BTC_USDT_PERP"]
        }
        await self._send_message(subscribe_message)

    async def subscribe_to_FundingRate(self):

        subscribe_message = {
            "event": "subscribe",
            "channel": ["funding_rate"],
            "symbols": ["BTC_USDT_PERP"]
        }
        await self._send_message(subscribe_message)
