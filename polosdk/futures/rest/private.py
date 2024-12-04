from pyclbr import Class

from polosdk.futures.rest.request import Request

class Private:
    def __init__(self, api_key, api_secret, url=None):
        self._request = Request(api_key, api_secret, url)

    def get_account_balance(self):
        return self._request('GET',f'/v3/account/balance', True)


    def place_order(self, symbol, side, order_type, sz, mgnMode, posSide, clOrdId=None, px=None, reduceOnly=False, timeInForce='GTC',
                    stpMode='NONE'):
        # 参数验证
        if side not in ['BUY', 'SELL']:
            raise ValueError("side must be 'BUY' or 'SELL'")
        if order_type not in ['MARKET', 'LIMIT', 'LIMIT_MAKER']:
            raise ValueError("type must be 'MARKET', 'LIMIT', or 'LIMIT_MAKER'")

        # 构建请求体
        order_data = {
            'symbol': symbol,
            'mgnMode': mgnMode,
            'posSide': posSide,
            'side': side,
            'type': order_type,
            'sz': sz,
            'reduceOnly': reduceOnly,
            'timeInForce': timeInForce,
            'stpMode': stpMode
        }

        if clOrdId:
            order_data['clOrdId'] = clOrdId
        if px and order_type in ['LIMIT', 'LIMIT_MAKER']:
            order_data['px'] = px

        # 发送请求
        return self._request('POST', '/v3/trade/order', True, body=order_data)

    def place_multiple_orders(self, orders):
        # 参数验证
        if not isinstance(orders, list) or not orders:
            raise ValueError("orders must be a non-empty list")

        for order in orders:
            if not isinstance(order, dict):
                raise ValueError("Each order must be a dictionary")
            if 'symbol' not in order:
                raise ValueError("Each order must have a 'symbol'")
            if 'side' not in order or order['side'] not in ['BUY', 'SELL']:
                raise ValueError("Each order must have a 'side' and it must be 'BUY' or 'SELL'")
            if 'type' not in order or order['type'] not in ['MARKET', 'LIMIT', 'LIMIT_MAKER']:
                raise ValueError("Each order must have a 'type' and it must be 'MARKET', 'LIMIT', or 'LIMIT_MAKER'")
            if 'sz' not in order:
                raise ValueError("Each order must have a 'sz' (size)")
            if 'mgnMode' not in order:
                raise ValueError("Each order must have a 'mgnMode'")
            if 'posSide' not in order:
                raise ValueError("Each order must have a 'posSide'")

        # 发送请求
        return self._request('POST', '/v3/trade/orders', True, body=orders)


    def cancel_order(self, symbol, **kwargs):
        if symbol is None:
            raise ValueError("symbol is need")
        params = {}
        params.update(kwargs)
        params.update({'symbol': symbol})
        return self._request('DELETE', '/v3/trade/order', True, params=params)

    def cancel_multiple_order(self, symbol, ordIds=None, clOrdIds=None):
        if symbol is None:
            raise ValueError("symbol is needed")

        if ordIds is None and clOrdIds is None:
            raise ValueError("Either ordIds or clOrdIds must be provided")

        # 构建请求体
        body = {'symbol': symbol}

        if ordIds is not None:
            body['ordIds'] = ordIds
        if clOrdIds is not None and ordIds is None:
            body['clOrdIds'] = clOrdIds

        print(body)

        # 发送请求，使用 body 传递参数
        return self._request('DELETE', '/v3/trade/batchOrders', True, body=body)

    def cancel_all_order(self, **kwargs):
        params = {}
        params.update(kwargs)
        return self._request('DELETE', '/v3/trade/allOrders', True, params=params)


    def close_at_market_price(self, symbol, mgnMode, **kwargs):
        if symbol is None:
            raise ValueError("symbol is need")
        params = {}
        params.update(kwargs)
        params.update({'symbol': symbol})
        params.update({'mgnMode': mgnMode})
        return self._request('POST', '/v3/trade/position', True, body=params)


    def close_all_at_market_price(self):
        return self._request('POST', '/v3/trade/positionAll', True)


    def get_current_orders(self, **kwargs):
        params = {}
        params.update(kwargs)
        return self._request('GET', '/v3/trade/order/opens', True, params=params)


    def get_execution_details(self, **kwargs):
        params = {}
        params.update(kwargs)
        return self._request('GET', '/v3/trade/order/trades', True, params=params)


    def get_order_history(self, **kwargs):
        params = {}
        params.update(kwargs)
        return self._request('GET', '/v3/trade/order/history', True, params=params)


    def get_current_position(self, **kwargs):
        params = {}
        params.update(kwargs)
        return self._request('GET', '/v3/trade/position/opens', True, params=params)


    def get_position_history(self, **kwargs):
        params = {}
        params.update(kwargs)
        return self._request('GET', '/v3/trade/position/history', True, params=params)


    def adjust_margin(self, symbol, amt, type, posSide = None):
        if symbol is None:
            raise ValueError("symbol is need")
        if amt is None or type is None:
            raise ValueError("amt or type is need")
        params = {}
        params.update({'symbol': symbol})
        params.update({'amt': amt})
        params.update({'type': type})
        if posSide != None:
            params.update({'posSide': posSide})
        return self._request('POST', '/v3/trade/position/margin', True, body=params)


    # def switch_cross(self, symbol, mgnMode):
    #     if symbol is None or mgnMode is None:
    #         raise ValueError("symbol or mgnMode is need")
    #     params = {}
    #     params.update({'symbol': symbol})
    #     params.update({'mgnMode': mgnMode})
    #     return self._request('POST', '/v3/position/switchIsolated', True, body=params)


    # def get_margin_mode(self, symbol):
    #     if symbol is None:
    #         raise ValueError("symbol is need")
    #     params = {}
    #     params.update({'symbol': symbol})
    #     return self._request('GET', '/v3/position/marginType', True, params=params)


    # def get_leverge(self, symbol):
    #     if symbol is None:
    #         raise ValueError("symbol is need")
    #     params = {}
    #     params.update({'symbol': symbol})
    #     return self._request('GET', '/v3/position/leverage', True, params=params)


    def set_leverge(self, symbol, lever, mgnMode, posSide):
        if symbol is None or lever is None:
            raise ValueError("symbol  or lever is need")
        params = {}
        params.update({'symbol': symbol})
        params.update({'lever': lever})
        params.update({'mgnMode': mgnMode})
        params.update({'posSide': posSide})
        return self._request('POST', '/v3/position/leverage', True, body=params)

    def set_position_mode(self, posMode):
        if posMode is None:
            raise ValueError("symbol  or lever is need")
        params = {}
        params.update({'posMode': posMode})
        return self._request('POST', '/v3/position/mode', True, body=params)

    def get_position_mode(self):
        params = {}
        return self._request('GET', '/v3/position/mode', True, params=params)

    def get_leverges(self, symbol, mgnMode):
        if symbol is None:
            raise ValueError("symbol is need")
        params = {}
        params.update({'symbol': symbol})
        params.update({'mgnMode': mgnMode})
        return self._request('GET', '/v3/position/leverages', True, params=params)