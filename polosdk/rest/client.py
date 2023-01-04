from polosdk.rest.accounts import Accounts
from polosdk.rest.subaccounts import Subaccounts
from polosdk.rest.markets import Markets
from polosdk.rest.request import Request
from polosdk.rest.orders import Orders
from polosdk.rest.smartorders import SmartOrders
from polosdk.rest.wallets import Wallets


class Client:
    """
    Main REST client used for accessing POLO trading api.

    Attributes:
        _accounts (Accounts): Class to handle all endpoints related to accounts.
        _markets (Markets): Class to handle all endpoints related to markets.
        _request (Request): Class used to handle REST requests.
        _orders (Orders): Class to handle all endpoints related to orders.
        _smartorders (SmartOrders): Class to handle all endpoints related to smart orders.
        _wallets (Wallets): Class to handle all endpoints related to wallets.
    """
    def __init__(self, api_key=None, api_secret=None, url=None):
        """
        Args:
            api_key (str, required): User api key used for authentication. Not required if using markets or currency
                                     endpoints.
            api_secret (str, required): User api secret used for authentication. Not required if using markets or
                                        currency endpoints.
            url (str, optional): Url for endpoints, default is set to PROD in Request class.
        """
        self._accounts = Accounts(api_key, api_secret, url)
        self._subaccounts = Subaccounts(api_key, api_secret, url)
        self._markets = Markets(url)
        self._request = Request(url=url)
        self._orders = Orders(api_key, api_secret, url)
        self._smartorders = SmartOrders(api_key, api_secret, url)
        self._wallets = Wallets(api_key, api_secret, url)

    def get_market(self, symbol):
        """
        Get a symbols info and its tradeLimit info.

        Args:
            symbol (str, required): Symbol name.

        Returns:
            A json object with the symbol and its tradeLimit info:
            {
                'symbol': (str) Symbol name,
                'baseCurrencyName': (str) Base currency name,
                'quoteCurrencyName': (str) Quote currency name,
                'displayName': (str) Symbol display name,
                'state': (str) Possible states(UNKNOWN, NORMAL, PAUSE, OFFLINE, NEW, POST_ONLY, ALL),
                'visibleStartTime': (int) Symbol visible start time,
                'tradableStartTime': (int) Symbol tradable start time,
                'symbolTradeLimit': {
                    'symbol': (str) Symbol name,
                    'priceScale': (int) Decimal precision for price,
                    'quantityScale': (int) Decimal precision for quantity,
                    'amountScale': (int) Decimal precision for amount,
                    'minQuantity': (str) Minimum required quantity,
                    'minAmount': (str) Minimum required amount,
                    'highestBid': (str) Maximum allowed bid,
                    'lowestAsk': (str) Minimum allowed ask,
                    'scales': (str[]) List of allowed scales
                },
                'crossMargin': {
                    'supportCrossMargin': (bool) Indicates if symbol supports cross margin,
                    'maxLeverage': (int) Maximum supported leverage
                }
            }

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.ref_data().get_market('BTC_USDT')
            print(response)
        """
        return self._request('GET', f'/markets/{symbol}')

    def get_markets(self):
        """
        Get all symbols and their tradeLimit info.

        Returns:
            A List of json objects with symbols and their tradeLimit info:
            [
                {
                    'symbol': (str) Symbol name,
                    'baseCurrencyName': (str) Base currency name,
                    'quoteCurrencyName': (str) Quote currency name,
                    'displayName': (str) Symbol display name,
                    'state': (str) Possible states(UNKNOWN, NORMAL, PAUSE, OFFLINE, NEW, POST_ONLY, ALL),
                    'visibleStartTime': (int) Symbol visible start time,
                    'tradableStartTime': (int) Symbol tradable start time,
                    'symbolTradeLimit': {
                        'symbol': (str) Symbol name,
                        'priceScale': (int) Decimal precision for price,
                        'quantityScale': (int) Decimal precision for quantity,
                        'amountScale': (int) Decimal precision for amount,
                        'minQuantity': (str) Minimum required quantity,
                        'minAmount': (str) Minimum required amount,
                        'highestBid': (str) Maximum allowed bid,
                        'lowestAsk': (str) Minimum allowed ask
                    },
                    'crossMargin': {
                        'supportCrossMargin': (bool) Indicates if symbol supports cross margin,
                        'maxLeverage': (int) Maximum supported leverage
                    }
                },
                {...},
                ...
            ]

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.ref_data().get_markets()
            print(response)
        """
        return self._request('GET', '/markets')

    def get_currency(self, currency, multichain=False):
        """
        Get data for a supported currency.

        Args:
            currency (str, required): Currency name.
            multichain (bool, optional): Default is false. Indicates if multi chain currencies are
                                         included. If set to true, additionally adds a new row for each
                                         currency on their respective chain (i.e USDT, USDTETH,
                                         USDTTRON will all have entries).

        Returns:
            A json object with the currency information:
            {
                'id': (int) Currency id,
                'name': (str) Currency name,
                'description': (str) The type of blockchain the currency runs on,
                'type': (str) Currency type,
                'withdrawalFee': (str) The network fee necessary to withdraw this currency,
                'minConf': (int) The minimum number of blocks necessary before a deposit can be credited to an account,
                'depositAddress': (str) If available, the deposit address for this currency,
                'blockchain': (int) The blockchain the currency runs on,
                'delisted': (bool) Designates whether (true) or not (false) this currency has been delisted from the exchange,
                'tradingState': (str) Currency trading state: NORMAL or OFFLINE,
                'walletState': (str) Currency state: ENABLED or DISABLED,
                'parentChain': (str) Only displayed when includeMultiChainCurrencies is set to true. The parent chain,
                'isMultiChain': (bool) Only displayed when includeMultiChainCurrencies is set to true. Indicates whether (true) or not (false) this currency is a multi chain,
                'isChildChain': (bool) If available, the deposit address for this currency,
                'childChains': (str[]) only displayed when includeMultiChainCurrencies is set to true. The child chains
            }

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.public().reference_data().get_currency('BTC')
            print(response)
        """
        params = {'includeMultiChainCurrencies': multichain}
        return self._request('GET', f'/currencies/{currency}', params=params)

    def get_currencies(self, multichain=False):
        """
        Get all supported currencies.

        Args:
            multichain (bool, optional): Default is false. Indicates if multi chain currencies are
                                         included. If set to true, additionally adds a new row for each
                                         currency on their respective chain (i.e USDT, USDTETH,
                                         USDTTRON will all have entries).

        Returns:
            A list of json objects with the information on currencies:
        [
            {
                'id': (int) Currency id,
                'name': (str) Currency name,
                'description': (str) The type of blockchain the currency runs on,
                'type': (str) Currency type,
                'withdrawalFee': (str) The network fee necessary to withdraw this currency,
                'minConf': (int) The minimum number of blocks necessary before a deposit can be credited to an account,
                'depositAddress': (str) If available, the deposit address for this currency,
                'blockchain': (int) The blockchain the currency runs on,
                'delisted': (bool) Designates whether (true) or not (false) this currency has been delisted from the exchange,
                'tradingState': (str) Currency trading state: NORMAL or OFFLINE,
                'walletState': (str) Currency state: ENABLED or DISABLED,
                'parentChain': (str) Only displayed when includeMultiChainCurrencies is set to true. The parent chain,
                'isMultiChain': (bool) Only displayed when includeMultiChainCurrencies is set to true. Indicates whether (true) or not (false) this currency is a multi chain,
                'isChildChain': (bool) If available, the deposit address for this currency,
                'childChains': (str[]) only displayed when includeMultiChainCurrencies is set to true. The child chains
            },
            {...},
            ...
        ]

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.ref_data().get_currencies(multichain=True)
            print(response)
        """
        params = {'includeMultiChainCurrencies': multichain}
        return self._request('GET', '/currencies', params=params)

    def get_timestamp(self):
        """
        Get current server time.

        Returns:
            A json object with server time:
            {
                'serverTime': (int) Server time
            }

        Raises:
            RequestError: An error occurred communicating with trade engine.

        Example:
            response = client.ref_data().get_timestamp()
            print(response)
        """
        return self._request('GET', '/timestamp')

    def accounts(self):
        """
        Returns:
            The account class used to make balance and fee info queries.
        """
        return self._accounts

    def subaccounts(self):
        """
        Returns:
            The subaccount class used to make subaccount queries.
        """
        return self._subaccounts

    def markets(self):
        """
        Returns:
             The markets class used for querying market information.
        """
        return self._markets

    def orders(self):
        """
        Returns:
             The orders class used for all api calls related to orders.
        """
        return self._orders

    def smartorders(self):
        """
        Returns:
             The smartorders class used for all api calls related to smartorders.
        """
        return self._smartorders

    def wallets(self):
        """
        Returns:
             The wallets class used for querying private trade information.
        """
        return self._wallets
