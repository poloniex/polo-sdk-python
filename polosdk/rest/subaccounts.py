from polosdk.rest.request import Request


class Subaccounts:
    """
    SubAccounts class handles all endpoints related to subaccounts.
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
        Get a list of all the accounts within an Account Group for a user.

        Returns:
            A list of json objects with account information:
            [
                {
                    'accountId': (str) External account ID,
                    'accountName': (str) Name of the account,
                    'accountState': (str) Account's state, e.g. NORMAL, LOCKED,
                    'isPrimary': (str) True if account is primary; False if a subaccount
                },
                {...},
                ...
            ]

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.subaccounts().get_accounts()
            print(response)
        """
        return self._request('GET', '/subaccounts', True)

    def get_balances(self):
        """
        Get balances information by currency and account type (SPOT and FUTURES) for each account in the account group.
        This is only functional for a primary user. A subaccount user can call /accounts/balances for SPOT account type
        and the futures API overview for its FUTURES balances.

        Returns:
            A list of json objects with account information:
            [
                {
                    'accountId': (str) External account ID,
                    'accountName': (str) Name of the account,
                    'accountType': (str) Account type. Currently only SPOT or FUTURES,
                    'isPrimary': (str) True if account is primary; False if a subaccount,
                    'balances':
                    [
                        {
                            ...
                        },
                        {...}
                    ]
                },
                {...},
                ...
            ]

            Balances for spot account:
            {
                'currency': (str) Currency name,
                'available': (str) Available amount for the currency. can be negative due to margin,
                'hold': (str) Frozen amount for the currency,
                'maxAvailable': (str) Amount of currency that can be transferred
            }

            Balances for future account:
            {
                'currency': (str) Currency name,
                'accountEquity': (str) Equal to margin Balance + unrealised PNL,
                'unrealisedPNL': (str) Unrealised profit and loss,
                'marginBalance': (str) Equal to positionMargin + orderMargin + frozenFunds + availableBalance,
                'positionMargin': (str) Position margin,
                'orderMargin': (str) Order margin,
                'frozenFunds': (str) Frozen funds,
                'availableBalance': (str) Available balance,
                'pnl': (str) Realised profit and loss
            }

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.accounts().get_balances()
            print(response)
        """

        return self._request('GET', '/subaccounts/balances', True)

    def get_account_balances(self, account_id):
        """
        Get balances information by account_id. This is only functional for a primary user.
        A subaccount user can call /accounts/balances for SPOT account type and the futures API overview for its FUTURES
        balances.

        Args:
            account_id (int): Account id

        Returns:
            A list of json objects with account information:
            {
                'accountId': (str) External account ID,
                'accountName': (str) Name of the account,
                'accountType': (str) Account type. Currently only SPOT or FUTURES,
                'isPrimary': (str) True if account is primary; False if a subaccount
                'balances':
                [
                    {
                        ...
                    },
                    {...}
                ]
            }

            Balances for spot account:
            {
                'currency': (str) Currency name,
                'available': (str) Available amount for the currency. can be negative due to margin,
                'hold': (str) Frozen amount for the currency,
                'maxAvailable': (str) Amount of currency that can be transferred
            }

            Balances for future account:
            {
                'currency': (str) Currency name,
                'accountEquity': (str) Equal to margin Balance + unrealised PNL,
                'unrealisedPNL': (str) Unrealised profit and loss,
                'marginBalance': (str) Equal to positionMargin + orderMargin + frozenFunds + availableBalance,
                'positionMargin': (str) Position margin,
                'orderMargin': (str) Order margin,
                'frozenFunds': (str) Frozen funds,
                'availableBalance': (str) Available balance,
                'pnl': (str) Realised profit and loss
            }

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.accounts().get_account_balances(<accountId>)
            print(response)
        """
        return self._request('GET', f'/subaccounts/{account_id}/balances', True)

    def transfer(self, currency, amount, from_account_id, from_account_type, to_account_id, to_account_type):
        """
        Transfer amount of currency from an account and account type to another account and account type among the
        accounts in the account group. Primary account can transfer to and from any subaccounts as well as transfer
        between 2 subaccounts across account types. Subaccount can only transfer to the primary account across account
        types.

        Args:
            currency (str, required): The currency to transfer, like USDT.
            amount (str, required): The amount to transfer.
            from_account_id (str, required): The account, from which the currency is transferred.
            from_account_type (str, required): 	From account type. (SPOT or FUTURES)
            to_account_id (str, required): The account, to which the currency is transferred.
            to_account_type (str, required): To account type. (SPOT or FUTURES)

        Returns:
            Reference Transfer Id:
            {
                'transferId': (str) Transfer ID
            }

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.accounts().transfer('USD', '2', '123', 'SPOT', '1234', 'SPOT')
            print(response)
        """
        body = {
            'currency': currency,
            'amount': amount,
            'fromAccountId': from_account_id,
            'fromAccountType': from_account_type,
            'toAccountId': to_account_id,
            'toAccountType': to_account_type
        }
        return self._request('POST', '/subaccounts/transfer', True, body=body)

    def get_transfers(self, begins_from=None, start_time=None, end_time=None, from_account_id=None,
                      from_account_type=None, to_account_id=None, to_account_type=None, **kwargs):
        """
        Get a list of transfer records of a user. Max interval for start and end time is 6 months.
        If no start/end time params are specified then records for last 7 days will be returned.

        Args:
            begins_from (int, optional): It is 'transferId'. The query begin at ‘from', and the default is 0.
            start_time (int, optional): Transfers before start time will not be retrieved. (milliseconds since UNIX epoch)
            end_time (int, optional): Transfers after end time will not be retrieved. (milliseconds since UNIX epoch)
            from_account_id (int, optional): External UID of the from account.
            from_account_type (str, optional): From account type. (SPOT or FUTURES)
            to_account_id (int, optional): External UID of the to account.
            to_account_type (str, optional): To account type. (SPOT or FUTURES)

        Keyword Args:
            limit (int, optional): The max number of records could be returned. Default is 100 and max is 1000 records.
            direction (str, optional): PRE, NEXT, default is NEXT.
            currency (str, optional): The transferred currency, like USDT. Default is for all currencies, if not specified.

        Returns:
            List of json objects with account transfer information:
            [
                {
                    'id': (str) Transfer ID,
                    'fromAccountId': (str) External UID of the from account,
                    'fromAccountName': (str) Name of the from account,
                    'fromAccountType': (str) From account type (SPOT or FUTURES),
                    'toAccountId': (str) External UID of the to account,
                    'toAccountType': (str) To account type (SPOT or FUTURES),
                    'toAccountName': (str) Name of the from account,
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
            response = client.subaccounts().get_transfers()
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

        if from_account_id is not None:
            params.update({'fromAccountId': from_account_id})

        if from_account_type is not None:
            params.update({'fromAccountType': from_account_type})

        if to_account_id is not None:
            params.update({'toAccountId': to_account_id})

        if to_account_type is not None:
            params.update({'toAccountType': to_account_type})

        return self._request('GET', '/subaccounts/transfer', True, params=params)

    def get_transfer(self, transfer_id):
        """
        Get a transfer record of a user by id.

        Args:
            transfer_id (str, required): Transfer ID.

        Returns:
            Json object with account transfer information:
            {
                'id': (str) Transfer ID,
                'fromAccountId': (str) External UID of the from account,
                'fromAccountName': (str) Name of the from account,
                'fromAccountType': (str) From account type (SPOT or FUTURES),
                'toAccountId': (str) External UID of the to account,
                'toAccountType': (str) To account type (SPOT or FUTURES),
                'toAccountName': (str) Name of the from account,
                'currency': (str) The transferred currency,
                'amount': (str) The transferred amount,
                'state': (str) The state of transfer operation (SUCCESS),
                'createTime': (int) The datetime of transfer operation
            }

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.subaccounts().get_transfer('501')
            print(response)
        """
        return self._request('GET', f'/subaccounts/transfer/{transfer_id}', True)
