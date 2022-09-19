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

    def get_transfers(self, **kwargs):
        """
        Get a list of transfer records of a user.

        Keyword Args:
            limit (int, optional): The max number of records could be returned.
            from (int, optional): It is 'transferId'. The query begin at ‘from', and the default is 0.
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
        return self._request('GET', '/accounts/transfer', True, kwargs)

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
