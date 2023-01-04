from polosdk.rest.request import Request


class Accounts:
    """
    Accounts class handles all endpoints related to account.

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

    def get_accounts(self):
        """
        Get a list of all accounts of a user.

        Returns:
            A list of json objects with account information:
            {
                'accountId': (str) Account ID,
                'accountType': (str) Account type. Currently only SPOT is supported,
                'accountState': (str) Account's state, e.g. NORMAL, LOCKED
            }

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.accounts().get_accounts()
            print(response)
        """
        return self._request('GET', '/accounts', True)

    def get_balances(self, account_type=None):
        """
        Get a list of all accounts of a user with each account’s id, type and balances (assets).

        Args:
            account_type (str, optional): The account type. e.g. SPOT. Default will show all account types if not
                                                 specified. Currently only SPOT is supported.

        Returns:
            A list of json objects with account information:
            [
                {
                    'accountId': (str) Account ID,
                    'accountType': (str) Account type. Currently only SPOT is supported,
                    'balances':
                    [
                        {
                            'currencyId': (str) Currency id,
                            'currency': (str) Currency name,
                            'available': (str) Available amount for the currency,
                            'hold': (str) Frozen amount for the currency
                        },
                        {...}
                    ]
                },
                {...},
                ...
            ]

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.accounts().get_balances()
            print(response)
        """
        params = {}
        if account_type is not None:
            params.update({'accountType': account_type})

        return self._request('GET', '/accounts/balances', True, params=params)

    def get_account_balances(self, account_id):
        """
        Get the full details for a single account with its balances: free (available) and locked (hold) for each currency.

        Args:
            account_id (int): Account id, data from /accounts.

        Returns:
            A list of json objects with account information:
            [
                {
                    'accountId': (str) Account ID,
                    'accountType': (str) Account type. Currently only SPOT is supported,
                    'balances':
                    [
                        {
                            'currencyId': (str) Currency id,
                            'currency': (str) Currency name,
                            'available': (str) Available amount for the currency,
                            'hold': (str) Frozen amount for the currency
                        },
                        {...}
                    ]
                }
            ]

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.accounts().get_account_balances(<accountId>)
            print(response)
        """
        return self._request('GET', f'/accounts/{account_id}/balances', True)

    def get_fee_info(self):
        """
        Get fee rate for an account.

        Returns:
            A list of json objects with account information:
            {
                'trxDiscount': (boolean) Discount exists if using TRX,
                'makerRate': (str) Maker rate,
                'takerRate': (str) Taker rate,
                'volume30D': (str) 30 days volume in USDT
            }

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.accounts().get_fee_info()
            print(response)
        """
        return self._request('GET', '/feeinfo', True)

    def transfer(self, currency, amount, from_account, to_account):
        """
        Transfer amount of currency from an account to another account for a user.

        Args:
            currency (str, required): The currency to transfer, like USDT.
            amount (str, required): The amount to transfer.
            from_account (str, required): The account, from which the currency is transferred.
            to_account (str, required): The account, to which the currency is transferred.

        Returns:
            Reference Transfer Id:
            {
                'transferId': (str) Transfer ID
            }

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
                response = client.accounts().transfer('USDT', '10.5', 'SPOT', 'FUTURES')
                print(response)
        """
        body = {
            'currency': currency,
            'amount': amount,
            'fromAccount': from_account,
            'toAccount': to_account
        }
        return self._request('POST', '/accounts/transfer', True, body=body)

    def get_transfers(self, begins_from=None, start_time=None, end_time=None, **kwargs):
        """
        Get a list of transfer records of a user.

        Args:
            begins_from (int, optional): It is 'transferId'. The query begin at ‘from', and the default is 0.
            start_time (int, optional): Transfers before start time will not be retrieved. (milliseconds since UNIX epoch)
            end_time (int, optional): Transfers after end time will not be retrieved. (milliseconds since UNIX epoch)

        Keyword Args:
            limit (int, optional): The max number of records could be returned.
            direction (str, optional): PRE, NEXT, default is NEXT.
            currency (str, optional): The transferred currency, like USDT. Default is for all currencies, if not specified.

        Returns:
            List of json objects with account transfer information:
            [
                {
                    'id': (str) Transfer ID,
                    'fromAccount': (str) The account, from which the currency is transferred,
                    'toAccount': (str) The account, to which the currency is transferred,
                    'currency': (str) The transferred currency,
                    'amount': (str) The transferred amount,
                    'state': (str) The state of transfer operation. (SUCCESS),
                    'createTime': (int) The datetime of transfer operation
                },
                {...},
                ...
            ]

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.accounts().get_transfers()
            print(response)
        """
        params = {}
        params.update(kwargs)
        if begins_from is not None:
            params.update({'from': begins_from})

        if start_time is not None:
            params.update({'startTime': start_time})

        if end_time is not None:
            params.update({'endTime': end_time})

        return self._request('GET', '/accounts/transfer', True, params=params)

    def get_transfer(self, transfer_id):
        """
        Get a transfer record of a user by id.

        Args:
            transfer_id (str, required): Transfer ID.

        Returns:
            Json object with account transfer information:
        {
            'id': (str) Transfer ID,
            'fromAccount': (str) The account, from which the currency is transferred,
            'toAccount': (str) The account, to which the currency is transferred,
            'currency': (str) The transferred currency,
            'amount': (str) The transferred amount,
            'state': (str) The state of transfer operation. (SUCCESS),
            'createTime': (int) The datetime of transfer operation
        }

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.accounts().get_transfer('501')
            print(response)
        """
        return self._request('GET', f'/accounts/transfer/{transfer_id}', True)

    def get_activity(self, start_time=None, end_time=None, activity_type=None, begins_from=None, **kwargs):
        """
        Get a list of activities such as airdrop, rebates, staking, credit/debit adjustments, and other (historical adjustments).

        Args
            start_time (int, optional): Trades filled before startTime will not be retrieved.(milliseconds since UNIX epoch)
            end_time (int, optional): Trades filled after endTime will not be retrieved.(milliseconds since UNIX epoch)
            activity_type (int, optional): Type of activity: ALL: 200, AIRDROP: 201, COMMISSION_REBATE: 202, STAKING: 203,
                                                             REFERAL_REBATE: 204, CREDIT_ADJUSTMENT: 104,
                                                             DEBIT_ADJUSTMENT: 105, OTHER: 199.  Must use numeric code.
            begins_from (int, optional): It is 'id'. The query begin at ‘from', and the default is 0.

        Keyword Args:
            limit (int, optional): The max number of records could be returned. Default is 100 and max is 1000.
            direction (str, optional): PRE, NEXT, default is NEXT.
            currency (str, optional): The transferred currency, like USDT. Default is for all currencies, if not specified.

        Returns:
            List of json objects with account activity information:
            [
                {
                    'id': (str) Activity ID,
                    'currency': (str) Currency like BTC, ETH etc,
                    'amount': (str) Amount of the activity (can be negative),
                    'state': (str) State of the activity (ex. SUCCESS),
                    'createTime': (int) Datetime of the activity,
                    'description': (str) Activity details,
                    'activityType': (int) type of activity
                },
                {...},
                ...
            ]

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.accounts().get_activity()
            print(response)
        """
        params = {}
        params.update(kwargs)

        if start_time is not None:
            params.update({'startTime': start_time})

        if end_time is not None:
            params.update({'endTime': end_time})

        if activity_type is not None:
            params.update({'activityType': activity_type})

        if begins_from is not None:
            params.update({'from': begins_from})

        return self._request('GET', '/accounts/activity', True, params=params)

    def get_margin(self, account_type='SPOT'):
        """
        Get account margin information

        Args:
            account_type (str, optional): The account type. Currently only SPOT is supported.

        Returns:
            Json objects with account margin information:
            {
                'totalAccountValue': (str) The sum of the usd value of all balances plus unrealized pnl,
                'totalMargin': (str) Collateral that can be used for margin,
                'usedMargin': (str) Amount of margin that has been used,
                'freeMargin': (str) Available free margin,
                'maintenanceMargin': (str) Minimum amount needed to keep account in good standing; enters liquidation mode if total margin falls below this value,
                'marginRatio': (str) Is calculated as total margin / maintenance Margin; account enters liquidation mode if this value < 100%,
                'time': (int) Time the record was created
            }

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.accounts().get_margin()
            print(response)
        """
        params = {'accountType': account_type}

        return self._request('GET', '/margin/accountMargin', True, params=params)

    def get_borrow_status(self, **kwargs):
        """
        Get borrow status of currencies.

        Keyword Args:
            currency (str, optional): Currency name.

        Returns:
            List of json objects with borrow status for currency:
            {
                'currency': (str) Currency name,
                'available': (str) Amount of available currency,
                'borrowed': (str) Borrowed amount,
                'hold': (str) Frozen amount,
                'maxAvailable': (str) Amount that can be withdrawn, including what's borrowable with margin,
                'hourlyBorrowRate': (str) Borrow rate per hour,
                'version': (str) Current version of the currency
            }

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.accounts().get_borrow_status()
            print(response)
        """
        params = {}
        params.update(kwargs)

        return self._request('GET', '/margin/borrowStatus', True, params=params)

    def get_margin_max(self, symbol):
        """
        Get maximum and available buy/sell amount for a given symbol.

        Args:
            symbol (str, required): Symbol name.

        Returns:
            Json objects with maximum and available buy/sell amount for a given symbol:
            {
                'symbol': (str) Symbol name,
                'maxLeverage': (int) Max leverage for the symbol,
                'availableBuy': (str) Available amount for the quote currency that can be bought,
                'maxAvailableBuy': (str) Maximum amount in quote currency that can be bought including margin,
                'availableSell': (str) Available amount for the base currency that can be sold,
                'maxAvailableSell': (str) Maximum amount in base currency that can be sold including margin
            }

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.accounts().get_margin_max('BTC_USDT')
            print(response)
        """
        params = {'symbol': symbol}

        return self._request('GET', '/margin/maxSize', True, params=params)
