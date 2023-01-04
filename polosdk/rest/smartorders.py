from polosdk.rest.request import Request


class SmartOrders:
    """
    Smart orders class handles all endpoints related to smart orders.

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

    def get_all(self, **kwargs):
        """
        Get a list of (pending) smart orders for an account.

        Keyword Args:
            limit (int, optional): The max number of smart orders could be returned.

        Returns:
            A list of json objects with smart order information:
            [
                {
                    'id': (str) Smart order id,
                    'clientOrderId': (str) User specified id or an empty string,
                    'symbol': (str) The symbol to trade, like BTC_USDT,
                    'state': (str) order state: PENDING_NEW,
                    'accountType': (str) Account type,
                    'side': (str) Possible sides(BUY, SELL),
                    'type': (str) Possible types(STOP, STOP_LIMIT),
                    'timeInForce': (str) Possible values(GTC, IOC, FOK),
                    'quantity': (str) Quote units to be traded for order,
                    'price': (str) Price for the order,
                    'amount': (str) Base units to be traded for order,
                    'stopPrice': (str) stop price,
                    'createTime': (int) Create time,
                    'updateTime': (int) Update time
                },
                {...}
                ...
            ]

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.smartorders().get_all()
            print(response)
        """
        return self._request('GET', '/smartorders', True, params=kwargs)

    def create(self, time_in_force=None, account_type=None, client_order_id=None, stop_price=None, **kwargs):
        """
        Create a smart order for an account.

        Args:
            time_in_force (str, optional): GTC, IOC, FOK (Default: GTC)
            account_type (str, optional): SPOT is the default and only supported one.
            client_order_id (str, optional): Custom client order id, Maximum 64-character length.
            stop_price (str, optional): Cannot be negative.

        Keyword Args:
            symbol (str, required): The symbol to trade, like BTC_USDT.
            side (str, required): Possible sides(BUY, SELL).
            quantity (str, required): Quote units to be traded for smart order. Cannot be negative.
            type (str, optional): STOP, STOP_LIMIT (Default: STOP if price not specified or STOP_LIMIT if price is
                                                    specified)
            price (str, optional): Required for STOP_LIMIT.
            amount (str, optional): Base units to be traded for smart order. Cannot be negative.

        Returns:
            json object with order id and client order id:
            {
                'id': (str) Smart order id,
                'clientOrderId': (str) ClientOrderId user specifies in request or an empty string
            }

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.smartorders().create(client_order_id='999999910',
                                                   time_in_force='FOK',
                                                   quantity='10',
                                                   side='BUY',
                                                   price='60100.00',
                                                   symbol='BTC_USDT',
                                                   type='STOP_LIMIT',
                                                   stop_price='60000.00')
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

        if stop_price is not None:
            body.update({'stopPrice': stop_price})

        return self._request('POST', '/smartorders', True, False, body=body)

    def cancel(self, symbol=None, account_type=None):
        """
        Batch cancel all smart orders in an account. symbol or account_type is required.

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
            Cancel all smart orders on 'BTC_USDT':
                response = client.smartorders().cancel(symbol='BTC_USDT')
                print(response)

            Cancel all smart orders on 'SPOT' account:
                response = client.smartorders().cancel(account_type='SPOT')
                print(response)
        """
        if symbol is None and account_type is None:
            raise ValueError('smartorders().cancel endpoint requires symbol or account_type')

        body = {}
        if symbol is not None:
            body.update({'symbol': symbol})

        if account_type is not None:
            body.update({'accountType': account_type})

        return self._request('DELETE', '/smartorders', True, False, body=body)

    def get_by_id(self, order_id=None, client_order_id=None):
        """
        Get a smart order’s status. {id} can be smart order’s id or its clientOrderId. If smart order’s state is
        TRIGGERED, the response will include the triggered order’s data. order_id or client_order_id is required.

        Args:
            order_id (str, optional): Order id
            client_order_id (str, optional): Client order id

        Returns:
            Json object with order's status:
            {
                'id': (str) Smart order id,
                'clientOrderId': (str) User specified id or an empty string,
                'symbol': (str) The symbol to trade, like BTC_USDT,
                'state': (str) order state: PENDING_NEW, PENDING_CANCEL, CANCELED, REJECTED, EXPIRED, TRIGGERED, FAILED,
                'accountType': (str) Account type,
                'side': (str) Possible sides(BUY, SELL),
                'type': (str) Possible types(STOP, STOP_LIMIT),
                'timeInForce': (str) Possible values(GTC, IOC, FOK),
                'quantity': (str) Quote units to be traded for smart order,
                'price': (str) Price for the order,
                'amount': (str) Base units to be traded for smart order,
                'stopPrice': (str) stop price,
                'createTime': (int) Create time,
                'updateTime': (int) Update time,
                'triggeredOrder': (json) The triggered order's data. This will only be displayed when the smart order's
                                         state is TRIGGERED.
            }

            triggeredOrder:
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
            Get smart order by client order id:
                response = client.smartorders().get_by_id(client_order_id='123Abc')
                print(response)

            Get smart order by order id:
                response = client.smartorders().get_by_id(order_id='21934611974062080')
                print(response)
        """
        if order_id is None and client_order_id is None:
            raise ValueError('get_by_id endpoint requires order_id or client_order_id')

        if order_id is not None:
            path = f'/smartorders/{order_id}'
        else:
            path = f'/smartorders/cid:{client_order_id}'

        return self._request('GET', path, True)

    def cancel_replace(self, order_id, time_in_force=None, proceed_on_failure=None, client_order_id=None, **kwargs):
        """
        Cancel an existing untriggered smart order and place a new smart order on the same symbol with details from
        existing smart order unless amended by new parameters. The replacement smart order can amend price, stopPrice,
        quantity, amount, type, and timeInForce fields. Specify the existing smart order id in the path; if id is a
        clientOrderId, prefix with cid: e.g. cid:myId-1. The proceedOnFailure flag is intended to specify whether to
        continue with new smart order placement in case cancelation of the existing smart order fails.

        Args:
            order_id (int, required): Id of original order
            client_order_id (str, optional): clientOrderId of the new order*
            time_in_force (str, optional): Amended timeInForce; GTC, IOC, FOK (Default: GTC)
            proceed_on_failure (str, optional): If set to true then new smart order will be placed even if cancelation
                                                of the existing smart order fails; if set to false (DEFAULT value) then
                                                new smart order will not be placed if the cancelation of the existing
                                                smart order fails.


        Keyword Args:
            price (str, optional): Amended price
            quantity (str, optional): Amended quantity
            amount (str, optional): Amended amount (needed for MARKET buy)
            type (str, optional): Amended type; MARKET, LIMIT, LIMIT_MAKER (for placing post only orders)

        Returns:
            json object with order id and client order id:
            {
                'id': (str) Smart order id,
                'clientOrderId': (str) ClientOrderId user specifies in request or an empty string
            }

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.smartorders().cancel_replace(order_id, price='19000', proceed_on_failure=True)
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

        return self._request('PUT', f'/smartorders/{order_id}', True, body=body)

    def cancel_by_id(self, order_id=None, client_order_id=None):
        """
        Cancel a smart order by its id. order_id or client_order_id is required.

        Args:
            order_id (str, optional): Smart order's id
            client_order_id (str, optional): Smart order's clientOrderId

        Returns:
            Json object with information on deleted order:
            {
                'orderId': (str) The smart order id,
                'clientOrderId': (str) clientOrderId of the order,
                'state': (str) Order's state (CANCELLED),
                'code': (int) Response code,
                'message': (str) Response message
            }

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            Cancel smart order by client order id:
                response = client.smartorders().cancel_by_id(client_order_id='123Abc')
                print(response)

            Cancel smart order by order id:
                response = client.smartorders().cancel_by_id(order_id='21934611974062080')
                print(response)
        """
        if order_id is None and client_order_id is None:
            raise ValueError('delete_by_id endpoint requires order_id or client_order_id')

        if order_id is not None:
            path = f'/smartorders/{order_id}'
        else:
            path = f'/smartorders/cid:{client_order_id}'

        return self._request('DELETE', path, True)

    def cancel_by_multiple_ids(self, order_ids=None, client_order_ids=None):
        """
        Batch cancel one or many active smart orders in an account by IDs. Order_ids or client_order_ids is required.

        Args:
            order_ids (str, optional): List of smart order ids
            client_order_ids (str, optional): List of client smart order ids

        Returns:
            List of json objects with information on deleted smart orders:
            [
                {
                    'orderId': (str) The smart order id,
                    'clientOrderId': (str) clientOrderId of the smart order,
                    'state': (str) smart Order's state (PENDING_CANCEL),
                    'code': (int) Response code,
                    'message': (str) Response message
                },
                {...},
                ...
            ]

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            Cancel multiple smart orders:
                response = client.smartorders().cancel_by_multiple_ids(
                                    order_ids=["12345", "67890"],
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

        return self._request('DELETE', '/smartorders/cancelByIds', True, body=body)

    def get_history(self, account_type=None, hide_cancel=None, start_time=None, end_time=None, begins_from=None, **kwargs):
        """
        Get a list of historical smart orders in an account.

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
            A list of json objects with smart order history information:
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
            response = client.smartorders().get_history(symbol='BTC_USDT')
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

        return self._request('GET', '/smartorders/history', True, params=params)
