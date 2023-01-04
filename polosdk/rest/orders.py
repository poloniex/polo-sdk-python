from polosdk.rest.request import Request


class Orders:
    """
    Orders class handles all endpoints related to orders.

    Attributes:
        _request (Request): Class used to handle REST requests.
    """

    def __init__(self, api_key, api_secret, url=None):
        """
        Args:
            api_key (str, required): User api key used for authentication.
            api_secret (str, required): User api secret used for authentication.
            url (str, optional): Url for endpoints, default is set to PROD in Request class.
        """
        self._request = Request(api_key, api_secret, url)

    def get_all(self, account_type=None, begins_from=None, **kwargs):
        """
        Get a list of active orders for an account.

        Args:
            account_type (str, optional): SPOT is the default and only supported one.
            begins_from (int, optional): It is 'orderId'. The query begin at 'from', and it is 0 when you first query.

        Keyword Args:
            symbol (str, optional): The symbol to trade,like BTC_USDT. Default is for all symbols if not specified.
            side (str, optional): Possible sides(BUY, SELL),
            direction (str, optional): Possible values(PRE, NEXT)
            limit (int, optional): The max number of orders could be returned.

        Returns:
            A list of json object's with order status':
            [
                {
                    'id': (str) Order id,
                    'clientOrderId': (str) User specified id or an empty string,
                    'symbol': (str) The symbol to trade, like BTC_USDT,
                    'state': (str) Possible states(PENDING_NEW, NEW, PARTIALLY_FILLED, FILLED, PENDING_CANCEL,
                                                   PARTIALLY_CANCELED, CANCELED, REJECTED, EXPIRED, FAILED),
                    'accountType': (str) Account type,
                    'side': (str) Possible sides(BUY, SELL),
                    'type': (str) Possible types(MARKET, LIMIT, LIMIT_MAKER),
                    'timeInForce': (str) Possible values(GTC, IOC, FOK),
                    'quantity': (str) Quote units to be traded for order,
                    'price': (str) Price for the order,
                    'avgPrice': (str) avgPrice = filledAmount/filledQuantity,
                    'amount': (str) Base units to be traded for order,
                    'filledQuantity': (str) Quote units already filled,
                    'filledAmount': (str) Base units already filled,
                    'createTime': (int) Create time,
                    'updateTime': (int) Update time
                },
                {...}
                ...
            ]

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.orders().get_all()
            print(response)
        """
        params = {}
        params.update(kwargs)

        if account_type is not None:
            params.update({'accountType': account_type})

        if begins_from is not None:
            params.update({'from': begins_from})

        return self._request('GET', '/orders', True, params=params)

    def create(self, time_in_force=None, account_type=None, client_order_id=None, allow_borrow=None, **kwargs):
        """
        Create an order for an account.

        Args:
            time_in_force (str, optional): GTC, IOC, FOK (Default: GTC)
            account_type (str, optional): SPOT is the default and only supported one.
            client_order_id (str, optional): Custom client order id, Maximum 64-character length
            allow_borrow (bool, optional): Allow order to be placed by borrowing funds (Default: false)

        Keyword Args:
            symbol (str, required): Controls aggregation by price
            side (str, required): BUY, SELL
            type (str, optional): MARKET, LIMIT, LIMIT_MAKER (Default: MARKET)
            price (str, optional): Price is required for non-market orders
            quantity (str, optional): Quantity is required for MARKET type and SELL side.
            amount (str, optional): Amount is required for MARKET and BUY side.

        Returns:
            Json object with order id and client order id:
            {
                'id': (str) Order id,
                'clientOrderId': (str) ClientOrderId user specifies in request or an empty string
            }

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            Limit Buy 0.00025 BTC_USDT at 18,000.00 when price hits 20000 USDT:
                 response = client.orders().create(client_order_id='123Abc',
                                                   price='18000',
                                                   stop_price='20000.00'
                                                   quantity='0.00025',
                                                   side='BUY',
                                                   symbol='BTC_USDT',
                                                   type='LIMIT',
                                                   time_in_force='IOC')
                 print(response)

            Market Buy 5 USDT worth of BTC on BTC_USDT:
                response = client.orders().create(side='BUY',
                                                  amount='5',
                                                  symbol='BTC_USDT')
                print(response)
        """
        body = {}
        body.update(kwargs)

        if time_in_force is not None:
            body.update({'timeInForce': time_in_force})

        if account_type is not None:
            body.update({'accountType': account_type})

        if client_order_id is not None:
            body.update({'clientOrderId': client_order_id})

        if allow_borrow is not None:
            body.update({'allowBorrow': allow_borrow})

        return self._request('POST', '/orders', True, body=body)

    def cancel(self, symbol=None, account_type=None):
        """
        Batch cancel all orders in an account. symbol or account_type is required.

        Args:
            symbol (str[], optional): If symbols are specified then all orders with those symbols will be canceled.
                                    If symbols are not specified or array is empty, it will cancel user's all orders
                                    for all symbols.
            account_type (str[], optional): SPOT is the only supported one.

        Returns:
            A list of json objects with information on all deleted orders:
            [
                {
                    'orderId': (str) The order id,
                    'clientOrderId': (str) clientOrderId of the order,
                    'state': (str) Order's state (PENDING_CANCEL),
                    'code': (int) Response code,
                    'message': (str) Response message
                },
                {...},
                ...
            ]

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            Cancel all orders on 'BTC_USDT':
                response = client.orders().cancel(symbol='BTC_USDT')
                print(response)

            Cancel all orders on 'SPOT' account:
                response = client.orders().cancel(account_type='SPOT')
                print(response)
        """
        if symbol is None and account_type is None:
            raise ValueError('orders().cancel endpoint requires symbol or account_type')

        body = {}
        if symbol is not None:
            body.update({'symbol': symbol})

        if account_type is not None:
            body.update({'accountType': account_type})

        return self._request('DELETE', '/orders', True, body=body)

    def get_by_id(self, order_id=None, client_order_id=None):
        """
        Get an order for an account. order_id or client_order_id is required.

        Args:
            order_id (str, optional): Order id
            client_order_id (str, optional): Client order id

        Returns:
            Json object with order's status:
            {
                'id': (str) Order id,
                'clientOrderId': (str) User specified id or an empty string,
                'symbol': (str) The symbol to trade, like BTC_USDT,
                'state': (str) Possible states(PENDING_NEW, NEW, PARTIALLY_FILLED, FILLED, PENDING_CANCEL,
                                               PARTIALLY_CANCELED, CANCELED, REJECTED, EXPIRED, FAILED),
                'accountType': (str) Account type,
                'side': (str) Possible sides(BUY, SELL),
                'type': (str) Possible types(MARKET, LIMIT, LIMIT_MAKER),
                'timeInForce': (str) Possible values(GTC, IOC, FOK),
                'quantity': (str) Quote units to be traded for order,
                'price': (str) Price for the order,
                'avgPrice': (str) avgPrice = filledAmount/filledQuantity,
                'amount': (str) Base units to be traded for order,
                'filledQuantity': (str) Quote units already filled,
                'filledAmount': (str) Base units already filled,
                'createTime': (int) Create time,
                'updateTime': (int) Update time
            }

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            Get order by client order id:
                response = client.orders().get_by_id(client_order_id='123Abc')
                print(response)

            Get order by order id:
                response = client.orders().get_by_id(order_id='21934611974062080')
                print(response)
        """
        if order_id is None and client_order_id is None:
            raise ValueError('get_by_id endpoint requires order_id or client_order_id')

        if order_id is not None:
            path = f'/orders/{order_id}'
        else:
            path = f'/orders/cid:{client_order_id}'

        return self._request('GET', path, True)

    def cancel_replace(self, order_id, time_in_force=None, proceed_on_failure=None, client_order_id=None,
                       allow_borrow=None, **kwargs):
        """
        Cancel an existing active order, new or partially filled, and place a new order on the same symbol with details
        from existing order unless amended by new parameters. The replacement order can amend price, quantity, amount,
        type, timeInForce, and allowBorrow fields. Specify the existing order id in the path; if id is a clientOrderId,
        prefix with cid: e.g. cid:myId-1. The proceedOnFailure flag is intended to specify whether to continue with new
        order placement in case cancelation of the existing order fails.
        Args:
            order_id (int, required): Id of original order
            client_order_id (str, optional): clientOrderId of the new order*
            time_in_force (str, optional): Amended timeInForce; GTC, IOC, FOK (Default: GTC)
            allow_borrow (bool, optional): Allow order to be placed by borrowing funds (Default: false)
            proceed_on_failure (str, optional): If set to true then new order will be placed even if cancelation of the
                                                existing order fails; if set to false (DEFAULT value) then new order
                                                will not be placed if the cancelation of the existing order fails.
        Keyword Args:
            price (str, optional): Amended price
            quantity (str, optional): Amended quantity
            amount (str, optional): Amended amount (needed for MARKET buy)
            type (str, optional): Amended type; MARKET, LIMIT, LIMIT_MAKER (for placing post only orders)
        Returns:
            Json object with order id and client order id:
            {
                'id': (str) Order id,
                'clientOrderId': (str) ClientOrderId user specifies in request or an empty string
            }
        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.orders().cancel_replace(order_id, price='19000', proceed_on_failure=True)
            print(response)
        """
        body = {}
        body.update(kwargs)

        if time_in_force is not None:
            body.update({'timeInForce': time_in_force})

        if proceed_on_failure is not None:
            body.update({'proceedOnFailure': proceed_on_failure})

        if client_order_id is not None:
            body.update({'clientOrderId': client_order_id})

        if allow_borrow is not None:
            body.update({'allowBorrow': allow_borrow})

        return self._request('PUT', f'/orders/{order_id}', True, body=body)

    def cancel_by_id(self, order_id=None, client_order_id=None):
        """
        Cancel an active order. Order_id or client_order_id is required, order_id is used if both are provided.

        Args:
            order_id (str, optional): Order's id
            client_order_id (str, optional): Order's clientOrderId

        Returns:
            Json object with information on deleted order:
            {
                'orderId': (str) The order id,
                'clientOrderId': (str) clientOrderId of the order,
                'state': (str) Order's state (PENDING_CANCEL),
                'code': (int) Response code,
                'message': (str) Response message
            }

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            Cancel order by client order id:
                response = client.orders().cancel_by_id(client_order_id='123Abc')
                print(response)

            Cancel order by order id:
                response = client.orders().cancel_by_id(order_id='21934611974062080')
                print(response)
        """
        if order_id is None and client_order_id is None:
            raise ValueError('get_by_id endpoint requires order_id or client_order_id')

        if order_id is not None:
            path = f'/orders/{order_id}'
        else:
            path = f'/orders/cid:{client_order_id}'

        return self._request('DELETE', path, True)

    def cancel_by_multiple_ids(self, order_ids=None, client_order_ids=None):
        """
        Batch cancel one or many active orders in an account by IDs. Order_ids or client_order_ids is required.

        Args:
            order_ids (str, optional): List of order ids
            client_order_ids (str, optional): List of client order ids

        Returns:
            List of json objects with information on deleted orders:
            [
                {
                    'orderId': (str) The order id,
                    'clientOrderId': (str) clientOrderId of the order,
                    'state': (str) Order's state (PENDING_CANCEL),
                    'code': (int) Response code,
                    'message': (str) Response message
                },
                {...},
                ...
            ]

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            Cancel order multiple orders:
                response = client.authenticated().orders().cancel_by_multiple_ids(order_ids=["12345", "67890"],
                                                                                  client_order_ids=["33344", "myId-1"])
                print(response)
        """
        if order_ids is None and client_order_ids is None:
            raise ValueError('cancel_by_multiple_ids endpoint requires order_ids or client_order_ids')

        body = {}
        if order_ids is not None:
            body.update({'orderIds': order_ids})

        if client_order_ids is not None:
            body.update({'clientOrderIds': client_order_ids})

        return self._request('DELETE', '/orders/cancelByIds', True, body=body)

    def get_history(self, account_type=None, hide_cancel=None, start_time=None, end_time=None, begins_from=None,
                    **kwargs):
        """
        Get a list of historical orders in an account.

        Args:
            account_type (str, optional): SPOT is the default and only supported one.
            hide_cancel (bool, optional): true or false. Whether canceled orders should not be retrieved.
                                         (Default: false)
            start_time (int, optional): (milliseconds since UNIX epoch) Orders updated before start_time will not be
                                        retrieved.
            end_time (int, optional): (milliseconds since UNIX epoch) Orders updated after end_time will not be retrieved.
            begins_from (int, optional): An 'orderId'. The query begins at ‘from'.

        Keyword Args:
            type (str, optional): MARKET, LIMIT, LIMIT_MAKER (Default: all types).
            side (str, optional): BUY, SELL (Default: both sides).
            symbol (str, optional): Any supported symbol (Default: all symbols).
            direction (str, optional): PRE, NEXT The direction before or after ‘from'.
            states (str, optional): FAILED, FILLED, CANCELED. PARTIALLY_CANCELED Multiple states can be specified and
                                    separated with comma. (Default: all states)
            limit (int, optional): The max number of orders could be returned. (Default: 100)

        Returns:
            A list of json objects with order history information:
            [
                {
                    'id': (str) Order id,
                    'clientOrderId': (str) User specified id,
                    'symbol': (str) The symbol the trade is for, like BTC_USDT,
                    'accountType': (str) Account type,
                    'side': (str) Possible sides(BUY, SELL),
                    'type': (str) Possible types(MARKET, LIMIT, LIMIT_MAKER),
                    'timeInForce': (str) Possible values(GTC, IOC, FOK),
                    'price': (str) Price for the order,
                    'avgPrice': (str) avgPrice = filledAmount/filledQuantity,
                    'quantity': (str) Quote units to be traded for order,
                    'amount': (str) Base units to be traded for order,
                    'filledQuantity': (str) Quote units already traded on order,
                    'filledAmount': (str) Base units already traded on order,
                    'state': (str) Possible states(PENDING_NEW, NEW, PARTIALLY_FILLED, FILLED, PENDING_CANCEL,
                                   PARTIALLY_CANCELED, CANCELED, REJECTED, EXPIRED, FAILED),
                    'orderSource': (str) Possible values(API, APP, WEB),
                    'createTime': (int) Create time,
                    'updateTime': (int) Update time
                },
                {...},
                ...
            ]

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.orders().get_history(symbol='BTC_USDT')
            print(response)
        """
        params = {}
        params.update(kwargs)

        if account_type is not None:
            params.update({'accountType': account_type})

        if hide_cancel is not None:
            params.update({'hideCancel': hide_cancel})

        if start_time is not None:
            params.update({'startTime': start_time})

        if end_time is not None:
            params.update({'endTime': end_time})

        if begins_from is not None:
            params.update({'from': begins_from})

        return self._request('GET', '/orders/history', True, params=params)

    def get_all_trades(self, end_time=None, start_time=None, begins_from=None, symbols=None, **kwargs):
        """
        Get a list of all trades for an account. Currently, trade history is supported since 07/30/2021. Interval
        between startTime and endTime cannot exceed 90 days. If only endTime is populated then startTime will default
        to 7 days before endTime. If only startTime is populated then endTime will be defaulted to 7 days after
        startTime.

        Args:
            end_time (int, optional): (milliseconds since UNIX epoch) Trades filled after endTime will not be retrieved.
            start_time (int, optional): (milliseconds since UNIX epoch) Trades filled before startTime will not be
                                       retrieved.
            begins_from (int, optional): It is 'orderId'. The query begin at 'from', and it is 0 when you first query. (use pageId value from response).
            symbols (str, optional): One or multiple symbols separated by comma e.g. BTC_USDT,ETH_USDT

        Keyword Args:
            limit (int, optional): Default and max value is 100.
            direction (str, optional): PRE, NEXT The direction before or after ‘from'.

        Returns:
            A list of json objects with all trades made for account:
            [
                {
                    'id': (str) Trade id,
                    'symbol': (str) The trading symbol, like BTC_USDT,
                    'accountType': (str) Account type,
                    'orderId': (str) The associated order's id,
                    'side': (str) Possible sides(BUY, SELL),
                    'type': (str) Possible types(MARKET, LIMIT, LIMIT_MAKER),
                    'matchRole': (str) Possible values(MAKER, TAKER),
                    'createTime': (int) Trade create time,
                    'price': (str) Price for the order,
                    'quantity': (str) Quote units,
                    'amount': (str) Base units,
                    'feeCurrency': (str) Fee currency name,
                    'feeAmount': (str) Fee amount
                },
                {...},
                ...
            ]

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.orders().get_all_trades(limit=5)
            print(response)
        """
        params = {}
        params.update(kwargs)

        if end_time is not None:
            params.update({'endTime': end_time})

        if start_time is not None:
            params.update({'startTime': start_time})

        if begins_from is not None:
            params.update({'from': begins_from})

        if symbols is not None:
            if type(symbols) == list:
                params.update({'symbols': ','.join(symbols)})
            else:
                params.update({'symbols': symbols})

        return self._request('GET', '/trades/', True, params=params)

    def get_trades(self, order_id):
        """
        Get a list of all trades for an order specified by its orderId.

        Args:
            order_id (str, required): The associated order's id.

        Returns:
            A list of json objects with all trades made for account:
            [
                {
                    'id': (str) Trade id,
                    'symbol': (str) The trading symbol, like BTC_USDT,
                    'accountType': (str) Account type,
                    'orderId': (str) The associated order's id,
                    'side': (str) Possible sides(BUY, SELL),
                    'type': (str) Possible types(MARKET, LIMIT, LIMIT_MAKER),
                    'matchRole': (str) Possible values(MAKER, TAKER),
                    'createTime': (int) Trade create time,
                    'price': (str) Price for the order,
                    'quantity': (str) Quote units,
                    'amount': (str) Base units,
                    'feeCurrency': (str) Fee currency name,
                    'feeAmount': (str) Fee amount,
                    'pageId': (str) A trade Id that can be used as query param 'from',
                    'clientOrderId': (str) Order's clientOrderId
                },
                {...},
                ...
            ]

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.orders().get_trades('21934611974062080')
            print(response)
        """
        return self._request('GET', f'/orders/{order_id}/trades', True)

    def set_kill_switch(self, timeout):
        """
        Kill switch mechanism allows to set a timer that cancels all regular and smartorders after the timeout has
        expired. Timeout can be reset by calling this command again with a new timeout value. A timeout value of -1
        disables the timer. Timeout is defined in seconds.

        Args:
            timeout (str, required): Timer value in seconds; range is -1 and 10 to 600.  Must be a number.

        Returns:
            A list of json objects with kill switch results:
            {
                'startTime': (int) Time when timer is started (milliseconds since UNIX epoch),
                'cancellationTime': (int) Time when timer is set to expire which will trigger cancellation (milliseconds since UNIX epoch)
            }

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.orders().set_kill_switch('15')
            print(response)
        """

        body = {'timeout': str(timeout)}
        return self._request('POST', '/orders/killSwitch', True, body=body)

    def get_kill_switch(self):
        """
        Get status of kill switch. If there is an active kill switch then the start and cancellation time is returned.
        If no active kill switch then an error message with code is returned.

        Returns:
            Json object with kill switch results:
            {
                'startTime': (int) Time when timer is started (milliseconds since UNIX epoch),
                'cancellationTime': (int) Time when timer is set to expire which will trigger cancellation (milliseconds since UNIX epoch)
            }

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.orders().get_kill_switch()
            print(response)
        """
        return self._request('GET', '/orders/killSwitchStatus', True)

    def create_multiple(self, orders):
        """
        Create multiple orders via a single request. Max limit of 20 orders.

        Args:
            orders ([{}], required): List of dictionaries, each item in list should contain parameters to create one
                                     order. Each order dictionary can have the following parameters
                                     {
                                        time_in_force (str, optional): GTC, IOC, FOK (Default: GTC)
                                        account_type (str, optional): SPOT is the default and only supported one.
                                        client_order_id (str, optional): Custom client order id, Maximum 64-character length
                                        symbol (str, required): Controls aggregation by price
                                        side (str, required): BUY, SELL
                                        type (str, optional): MARKET, LIMIT, LIMIT_MAKER (Default: MARKET)
                                        price (str, optional): Price is required for non-market orders
                                        quantity (str, optional): Quantity is required for MARKET type and SELL side.
                                        amount (str, optional): Amount is required for MARKET and BUY side.
                                    }

        Returns:
            List of json objects with order id and client order id:
            [
                {
                    'id': (str) Order id,
                    'clientOrderId': (str) ClientOrderId user specifies in request or an empty string
                },
                ...
            ]

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
        multi_order_request =
                [
                    {
                        'price': '20000',
                        'quantity': '0.00025',
                        'side': 'SELL',
                        'symbol': 'BTC_USDT',
                        'type': 'LIMIT'
                    },
                    {
                        'price': '50',
                        'quantity': '0.05',
                        'side': 'BUY',
                        'symbol': 'LTC_USDT',
                        'type': 'LIMIT'
                    },
                    {
                        'price': '22000',
                        'quantity': '0.00024',
                        'side': 'SELL',
                        'symbol': 'BTC_USDT',
                        'type': 'LIMIT'
                    }
                ]

        response = client.orders().create_multiple(multi_order_request)
        """
        body = []
        for order in orders:
            order_request = {}
            order_request.update(order)

            if 'time_in_force' in order_request.keys():
                order_request.update({'timeInForce': order_request['time_in_force']})
                order_request.pop('time_in_force')

            if 'account_type' in order_request.keys():
                order_request.update({'accountType': order_request['account_type']})
                order_request.pop('account_type')

            if 'client_order_id' in order_request.keys():
                order_request.update({'clientOrderId': order_request['client_order_id']})
                order_request.pop('client_order_id')

            body.append(order_request)

        return self._request('POST', '/orders/batch', True, body=body)
