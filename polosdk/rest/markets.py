from polosdk.rest.request import Request


class Markets:
    """
    Markets class allows read access to public market data.

    No authentication is necessary but you must not excessively use any API endpoint.

    Attributes:
        _request (Request): Class used to handle REST requests.
    """
    def __init__(self, url=None):
        """
        Args:
            url (str, optional): Url for endpoints, default is set to PROD in Request class.
        """
        self._request = Request(url=url)

    def get_candles(self, symbol, interval, start_time=None, end_time=None, **kwargs):
        """
        Returns OHLC for a symbol at given timeframe (interval).

        Args:
            symbol (str, required): Symbol name.
            interval (str, required): The unit of time to aggregate data by. Valid values: MINUTE_1, MINUTE_5,
                                      MINUTE_10, MINUTE_15, MINUTE_30, HOUR_1, HOUR_2, HOUR_4, HOUR_6, HOUR_12, DAY_1,
                                      DAY_3, WEEK_1 and MONTH_1.
            start_time (int, optional): Filters by time. The default value is 0.
            end_time (int, optional): Filters by time. The default value is current time.

        Keyword Args:
            limit (int, optional): Maximum number of records returned. The default value is 100 and the max value is
                                   500.


        Returns:
            The response is a list of candles data values displayed in an array in the following order:
                [
                    [
                        low (str): Lowest price over the interval,
                        high (str): Highest price over the interval,
                        open (str): Price at the start time,
                        close (str): Price at the end time,
                        amount (str): Quote units traded over the interval,
                        quantity (str): Base units traded over the interval,
                        buyTakerAmount (str): Quote units traded over the interval filled by market buy orders,
                        buyTakerQuantity (str): Base units traded over the interval filled by market buy orders,
                        tradeCount (int): Count of trades,
                        ts (int): Time the record was pushed,
                        weightedAverage (str): Weighted average over the interval,
                        interval (str): The selected interval,
                        startTime (int): Start time of interval,
                        closeTime (int): Close time of interval
                    ],
                    [...],
                    ...
                ]

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.market_data().get_candles('BTC_USDT', 'HOUR_4')
            print(response)
        """
        params = {'interval': interval}
        params.update(kwargs)

        if start_time is not None:
            params.update({'startTime': start_time})

        if end_time is not None:
            params.update({'endTime': end_time})


        return self._request('GET', f'/markets/{symbol}/candles', params=params)

    def get_orderbook(self, symbol, **kwargs):
        """
        Get the order book for a given symbol.

        Args:
            symbol (str, required): Symbol name.

        Keyword Args:
            scale (str, optional): Controls aggregation by price.
            limit (int, optional): Maximum number of records returned. The default value of limit is 10. Valid limit
                                   values are: 5, 10, 20, 50, 100, 150.


        Returns:
            A json object with the order book for the requested symbol:
                {
                    'time': (int) time the record was created,
                    'scale': (str) controls aggregation by price,
                    'asks': (str[]) list of asks,
                    'bids': (str[]) list of bids,
                    'ts': (int) time the record was pushed
                }

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.market_data().get_orderbook('BTC_USDT')
            print(response)
        """
        return self._request('GET', f'/markets/{symbol}/orderBook', params=kwargs)

    def get_price(self, symbol):
        """
        Get latest trade price for a symbol.

        Args:
            symbol (str, required): Symbol name.

        Returns:
            A json object with the latest price data:
                {
                    'symbol': (str) Symbol name,
                    'price': (str) Current price,
                    'time': (int) Time the record was created,
                    'dailyChange': (str) Daily change in decimal,
                    'ts': (int) Time the record was pushed
                }

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            ```python
                response = client.markets().get_price('BTC_USDT')
                print(response)
            ```
        """
        return self._request('GET', f'/markets/{symbol}/price')

    def get_prices(self):
        """
        Get latest trade price for all symbols.

        Returns:
            A list of json objects with the latest price data:
                [
                    {
                        'symbol': (str) Symbol name,
                        'price': (str) Current price,
                        'time': (int) Time the record was created,
                        'dailyChange': (str) Daily change in decimal,
                        'ts': (int) Time the record was pushed
                    },
                    {...},
                    ...
                ]

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.markets().get_prices()
            print(response)
        """
        return self._request('GET', '/markets/price')

    def get_ticker24h_all(self):
        """
        Retrieve ticker in last 24 hours for all symbols.

        Returns:
            A json object with a list of 24 hour ticker information:
                [
                    {
                        'symbol': (str) Symbol name,
                        'open': (str) Price at the start time,
                        'low': (str) Lowest price over the last 24h,
                        'high': (str) Highest price over the last 24h,
                        'close': (str) Price at the end time,
                        'quantity': (str) Base units traded over the last 24h,
                        'amount': (str) Quote units traded over the last 24h,
                        'tradeCount': (int) Count of trades,
                        'startTime': (int) Start time for the 24h interval,
                        'closeTime': (int) Close time for the 24h interval,
                        'displayName': (str) Symbol display name,
                        'dailyChange': (str) Daily change in decimal,
                        'ts': (int) Time the record was pushed
                    },
                    {...},
                    ...
                ]

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.market_data().get_ticker24h_all()
            print(response)
        """
        return self._request('GET', '/markets/ticker24h')

    def get_ticker24h(self, symbol):
        """
        Retrieve ticker in last 24 hours for a given symbol.

        Args:
            symbol (str, required): Symbol name.

        Returns:
            A json object with the 24 hour ticker information:
                {
                    'symbol': (str) Symbol name,
                    'open': (str) Price at the start time,
                    'low': (str) Lowest price over the last 24h,
                    'high': (str) Highest price over the last 24h,
                    'close': (str) Price at the end time,
                    'quantity': (str) Base units traded over the last 24h,
                    'amount': (str) Quote units traded over the last 24h,
                    'tradeCount': (int) Count of trades,
                    'startTime': (int) Start time for the 24h interval,
                    'closeTime': (int) Close time for the 24h interval,
                    'displayName': (str) Symbol display name,
                    'dailyChange': (str) Daily change in decimal,
                    'ts': (int) Time the record was pushed
                }

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.markets().get_ticker24h('BTC_USDT')
            print(response)
        """
        return self._request('GET', f'/markets/{symbol}/ticker24h')

    def get_trades(self, symbol, **kwargs):
        """
        Gets a list of recent trades.

        Args:
            symbol (str, required): Symbol name.

        Keyword Args:
            limit (int, optional): Maximum number of records returned. The default value is 500, and max value is 1000.

        Returns:
            A list of json objects with recent trades:
                [
                    {
                        'id': (str) Trade id,
                        'price': (str) Trade price,
                        'quantity': (str) Base units traded,
                        'amount': (str) Quote units traded,
                        'takerSide': (str) Taker's trade side (BUY, SELL),
                        'ts': (int) Time the trade was pushed,
                        'createTime': (int) Time the trade was created
                    },
                    {...},
                    ...
                ]

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.markets().get_trades('BTC_USDT')
            print(response)
        """
        return self._request('GET', f'/markets/{symbol}/trades', params=kwargs)
