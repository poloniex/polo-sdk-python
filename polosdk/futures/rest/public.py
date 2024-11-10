from polosdk.futures.rest.request import Request


class Public:
    def __init__(self, url=None):
        """
        Args:
            url (str, optional): Url for endpoints, default is set to PROD in Request class.
        """
        self._request = Request(url=url)

    def get_order_book(self,symbol,**kwargs):
        if symbol is None:
            raise ValueError("symbol is need")
        params = {}
        params.update(kwargs)
        params.update({'symbol': symbol})
        return self._request('GET', '/v3/market/orderBook', params=params)

    def get_k_line_data(self,symbol,interval,**kwargs):
        if symbol is None or interval is None:
            raise ValueError("symbol or interval is need")
        params = {}
        params.update(kwargs)
        params.update({'symbol': symbol})
        params.update({'interval': interval})
        return self._request('GET', '/v3/market/candles', params=params)

    def get_execution_info(self,symbol,**kwargs):
        if symbol is None:
            raise ValueError("symbol is need")
        params = {}
        params.update(kwargs)
        params.update({'symbol': symbol})
        return self._request('GET', '/v3/market/trades', params=params)
    def get_narket_info(self):
        return self._request('GET','/v3/market/tickers')

    def index_price(self,**kwargs):
        params = {}
        params.update(kwargs)
        return self._request('GET', '/v3/market/indexPrice', params=params)

    def get_index_price_components(self,symbol):
        if symbol is None:
            raise ValueError("symbol is need")
        params = {}
        params.update({'symbol': symbol})
        return self._request('GET', '/v3/market/indexPriceComponents', params=params)

    def get_index_price_k_line_data(self, symbol, interval, **kwargs):
        if symbol is None or interval is None:
            raise ValueError("symbol or interval is need")
        params = {}
        params.update(kwargs)
        params.update({'symbol': symbol})
        params.update({'interval': interval})
        return self._request('GET', '/v3/market/indexPriceCandlesticks', params=params)

    def get_premium_index_price_k_line_data(self, symbol, interval, **kwargs):
        if symbol is None or interval is None:
            raise ValueError("symbol or interval is need")
        params = {}
        params.update(kwargs)
        params.update({'symbol': symbol})
        params.update({'interval': interval})
        return self._request('GET', '/v3/market/premiumIndexCandlesticks', params=params)

    def get_mark_price(self,**kwargs):
        params = {}
        params.update(kwargs)
        return self._request('GET', '/v3/market/markPrice', params=params)

    def get_mark_price_k_line_data(self, symbol, interval, **kwargs):
        if symbol is None or interval is None:
            raise ValueError("symbol or interval is need")
        params = {}
        params.update(kwargs)
        params.update({'symbol': symbol})
        params.update({'interval': interval})
        return self._request('GET', '/v3/market/markPriceCandlesticks', params=params)

    def get_product_info(self,symbol):
        if symbol is None:
            raise ValueError("symbol is need")
        params = {}
        params.update({'symbol': symbol})
        return self._request('GET', '/v3/market/instruments', params=params)

    def get_current_funding_rate(self,symbol):
        if symbol is None:
            raise ValueError("symbol is need")
        params = {}
        params.update({'symbol': symbol})
        return self._request('GET', '/v3/market/fundingRate', params=params)

    def get_history_funding_rate(self,**kwargs):
        params = {}
        params.update(kwargs)
        return self._request('GET', '/v3/market/fundingRate/history', params=params)

    def get_current_open_positions(self,symbol):
        if symbol is None:
            raise ValueError("symbol is need")
        params = {}
        params.update({'symbol': symbol})
        return self._request('GET', '/v3/market/openInterest', params=params)

    def get_query_insurance_fund_information(self):
        return self._request('GET', '/v3/market/insurance')


    def get_futures_risk_limit(self,**kwargs):
        params = {}
        params.update(kwargs)
        return self._request('GET', '/v3/market/riskLimit', params=params)

