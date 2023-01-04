from polosdk.rest.request import Request
import time


class Wallets:
    """
    Class to handle all endpoints related to wallets.

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

    def get_deposit_addresses(self, currency=None):
        """
        Get all deposit addresses for a user.

        Args:
            currency (str, optional): The currency to display for the deposit address. If not specified, the deposit
                                      address of all currencies will be displayed.

        Returns:
            Dictionary of currency deposit address':
            {
                'currency': (str) The deposit address for the currency
                ...
            }

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.wallets().get_deposit_addresses()
            print(response)
        """
        params = {}
        if currency is not None:
            params = {'currency': currency}

        return self._request('GET', '/wallets/addresses', True, params=params)

    def get_activity(self, start=0, end=None, activity_type=None):
        """
        Get adjustment, deposit, and withdrawal activity history within a range window for a user.

        Args:
            start (int, optional): The start UNIX timestamp of activities in seconds.  Default 0.
            end (int, optional): The end UNIX timestamp of activities in seconds. Default current time.
            activity_type (str, optional): The type of activity: adjustments, deposits and withdrawals. If no activity
                                          type is specified, activities of all types will be returned.

        Returns:
            Json dictionary with all wallet activity:
        {
            'adjustments': (Json object) list of adjustments activities,
            'deposits': (Json object) list of deposits activities,
            'withdrawals': (Json object) list of withdrawals activities
        }

        adjustments Field:
        {
            'currency': (str) the currency of this adjustment,
            'amount': (str) the total value of the adjustment,
            'timestamp': (int) the UNIX timestamp when the adjustment was credited,
            'status': (str) adjustment status (only COMPLETE),
            'category': (str) always adjustment,
            'adjustmentTitle': (str) the type of adjustment,
            'adjustmentDesc': (str) a human-readable description of the adjustment,
            'adjustmentHelp': (str) a help center link to describe the adjustment
        }

        deposits Field:
        {
            'depositNumber': (int) the unique deposit ID for this deposit,
            'currency': (str) the currency of this deposit,
            'address': (int) the address to which this deposit was sent,
            'amount': (str) the total value of the deposit (network fees will not be included in this),
            'confirmations': (int) the total number of confirmations for this deposit,
            'txid': (str) the blockchain transaction ID of this deposit,
            'timestamp': (int) the UNIX timestamp when this deposit was first noticed,
            'status': (str) the current status of this deposit (either PENDING or COMPLETE)
        }

        withdrawals Field:
        {
            'withdrawalNumber': (int) the unique ID for this withdrawal,
            'currency': (str) the currency of this withdrawal,
            'address': (str) the address to which the withdrawal was made,
            'amount': (str) the total amount withdrawn including the fee,
            'fee': (str) the fee paid to the exchange for this withdrawal,
            'timestamp': (int) the Unix timestamp of the withdrawal,
            'status': (str) the status of the withdrawal (one of PENDING, AWAITING APPROVAL, COMPLETE or
                            COMPLETE ERROR) and optionally the transaction ID of the withdrawal,
            'ipAddress': (str) the IP address which initiated the withdrawal request,
            'paymentID': (str) the paymentID specified for this withdrawal. If none were specified, the field will
                               be null
        }

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.wallets().get_activity()
            print(response)
        """
        if end is None:
            end = int(time.time())

        params = {
            'start': start,
            'end': end
        }

        if activity_type is not None:
            params.update({'activityType': activity_type})

        return self._request('GET', '/wallets/activity', True, params=params)

    def create_address(self, currency):
        """
        Create a new address for a currency.

        Args:
            currency (str, required): The currency to use for the deposit address.

        Returns:
            Json object with newly created address':
            {
                'address': (str) The newly created address
            }

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.wallets().create_address('TRX')
            print(response)
        """
        body = {'currency': currency}
        return self._request('POST', '/wallets/address', True, body=body)

    def withdraw(self, currency, amount, address, payment_id=None, allow_borrow=None):
        """
        Immediately places a withdrawal for a given currency, with no email confirmation. In order to use this method,
        withdrawal privilege must be enabled for your API key.

        Some currencies use a common deposit address for everyone on the exchange and designate the account for which
        this payment is destined by populating paymentID field. In these cases, use /currencies to look up the
        mainAccount for the currency to find the deposit address and use the address returned by /wallets/addresses or
        generate one using /wallets/address as the paymentId. Note: currencies will only include a mainAccount property
        for currencies which require a paymentID.

        For currencies where there are multiple networks to choose from (like USDT or BTC), you can specify the chain by
        setting the "currency" parameter to be a multiChain currency name, like USDTTRON, USDTETH, or BTCTRON. You can
        get information on these currencies, like fees or if they"re disabled, by adding the
        "includeMultiChainCurrencies" optional parameter to the /currencies endpoint.

        Args:
            currency (str, required): Currency name.
            amount (str, required): Withdrawal amount.
            address (str, required): Withdrawal address.
            payment_id (str, optional): PaymentId for currencies that use a command deposit address.
            allow_borrow (bool, optional): Allow to transfer borrowed funds (Default: false)

        Returns:
            Json object with the withdrawal reference ID:
            {
                'withdrawalNumber': (int) The withdrawal reference ID
            }

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.wallets().withdraw(
                          'ETH', '1.50', '0xbb8d0d7c346daecc2380dabaa91f3ccf8ae232fb4')
            print(response)
        """
        body = {
            'currency': currency,
            'amount': amount,
            'address': address
        }

        if payment_id is not None:
            body.update({'paymentId': payment_id})

        if allow_borrow is not None:
            body.update({'allowBorrow': allow_borrow})

        return self._request('POST', '/wallets/withdraw', True, body=body)
