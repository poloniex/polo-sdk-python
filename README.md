## polo-sdk-python

Python 3 wrapper for Poloniex Exchange

Required Python version 3.7+

DISCLAIMER:
```
USE AT YOUR OWN RISK. You should not use this code in production unless you fully understand its limitations.
Even if you understand the code and its limitations, you may incur losses when using this code for trading.
When used in combination with your own code, the combination may not function as intended, and as a result you may incur losses.
Poloniex is not responsible for any losses you may incur when using this code.
```

## Features

- Support for REST and websocket endpoints
- Simple handling of authentication
- Response exception handling

## Getting Started

- Register an account with [Poloniex](<https://www.poloniex.com/signup>).
- Generate an [API Key](<https://poloniex.com/apiKeys>).
- Set environment variables that contain your API Key values: `POLO_API_KEY` and `POLO_API_SECRET`.
- [Get the source files](#source).
- For license refer to [LICENSE file](./LICENSE)

<a name="source"></a>Get the code files with git.

Clone the repo into the path you will be using
```bash
git clone https://github.com/poloniex/polo-sdk-python
```

### REST API

#### Public Methods
  - Instantiate a client
  ```python
  from polosdk import RestClient

  client = RestClient()
  ```
  - Symbol
  ```python
  # Get a symbols info and its tradeLimit info
  response = client.get_market('BTC_USDT')
  ```

  ```python
  # Get all symbols and their tradeLimit info
  response = client.get_markets()
  ```

  - Currency
  ```python
  # Get data for a supported currency
  response = client.get_currency('BTC')
  ```

  ```python
  # Get all supported currencies
  response = client.get_currencies(multichain=True)
  ```

  - System Timestamp
  ```python
  # Get all supported currencies
  response = client.get_timestamp()
  ```
#### Markets
  - Prices
  ```python
  # Get latest trade price for all symbols
  response = client.markets().get_prices()
  ```

  ```python
  # Get latest trade price for a symbol
  response = client.markets().get_price('BTC_USDT')
  ```

  - Order Book
  ```python
  # Get the order book for a given symbol
  response = client.markets().get_orderbook('BTC_USDT')
  ```

  - Candles
  ```python
  # Returns OHLC for a symbol at given timeframe (interval)
  response = client.markets().get_candles('BTC_USDT', 'HOUR_4')
  ```

  - Trades
  ```python
  # Gets a list of recent trades
  response = client.markets().get_trades('BTC_USDT')
  ```

  - Ticker
  ```python
  # Retrieve ticker in last 24 hours for a given symbol
  response = client.markets().get_ticker24h('BTC_USDT')
  ```

  ```python
  # Retrieve ticker in last 24 hours for all symbols
  response = client.markets().get_ticker24h_all()
  ```

#### Authenticated Methods

  - Instantiate a client
  ```python
  import os
  from polosdk import RestClient

  api_key = os.environ['POLO_API_KEY']
  api_secret = os.environ['POLO_API_SECRET']

  client = RestClient(api_key, api_secret)
  ```

#### Accounts
  - Account
  ```python
  # Get a list of all accounts of a user
  response = client.accounts().get_accounts()
  ```

  - Account Balances
  ```python
  # Get a list of all accounts of a user with each account’s id, type and balances (assets)
  response = client.accounts().get_balances()
  ```

  ```python
  # Get the full details for a single account with its balances
  response = client.accounts().get_account_balances('123')
  ```

  - Account Activity
  ```python
  # Get a list of activities such as airdrop, rebates, staking, credit/debit adjustments, and other (historical adjustments).
  response = client.accounts().get_activity()
  ```

  - Transfer Balances
  ```python
  # Transfer amount of currency from an account to another account for a user
  response = client.accounts().transfer('USDT', '10.5', 'SPOT', 'FUTURES')
  ```

  - Transfer Activity
  ```python
  # Get a list of transfer records of a user
  response = client.accounts().get_transfers()
  ```

  ```python
  # Get a transfer record of a user by id
  response = client.accounts().get_transfer('501')
  ```

  - Fee Info
  ```python
  # Get fee rate for an account
  response = client.accounts().get_fee_info()
  ```

#### Wallets
  - Deposit Addresses
  ```python
  # Get all deposit addresses for a user
  response = client.wallets().get_deposit_addresses()
  ```

  - Generate Address
  ```python
  # Create a new address for a currency
  response = client.wallets().create_address('TRX')
  ```

  - Withdraw Currency
  ```python
  # Immediately places a withdrawal for a given currency, with no email confirmation
  # In order to use this method, withdrawal privilege must be enabled for your API key
  response = client.wallets().withdraw('ETH', '1.50', '0x123abc')
  ```

  - Wallet Activity
  ```python
  # Get adjustment, deposit, and withdrawal activity history within a range window for a user
  response = client.wallets().get_activity()
  ```

#### Orders
  - Create Order
  ```python
  # Create a market order for 5 USDT of BTC
  response = client.orders().create(side='BUY', amount='5', symbol='BTC_USDT')
  ```

  ```python
  # Create a limit order for 0.00025 BTC at 20000 USDT
  response = client.orders().create(price='20000',
                                    quantity='0.00025',
                                    side='BUY',
                                    symbol='BTC_USDT',
                                    type='LIMIT',
                                    client_order_id='123Abc')
  ```

  - Open Orders
  ```python
  # Get a list of active orders for an account
  response = client.orders().get_all()
  ```

  - Order Details
  ```python
  # Create an order for an account

  # Get order by client order id
  response = client.orders().get_by_id(client_order_id='123Abc')

  # Get order by order id
  response = client.orders().get_by_id(order_id='21934611974062080')
  ```

  - Cancel Order by Id
  ```python
  # Cancel an active order

  # Cancel order by client order id
  response = client.orders().cancel_by_id(client_order_id='123Abc')

  # Cancel order by order id
  response = client.orders().cancel_by_id(order_id='21934611974062080')
  ```

  - Cancel Multiple Orders by Ids
  ```python
  # Batch cancel one or many active orders in an account by IDs
  response = client.orders().cancel_by_multiple_ids(
               order_ids=["12345", "67890"],
               client_order_ids=["33344", "myId-1"])
  ```

  - Cancel All Orders
  ```python
  # Batch cancel all orders in an account

  # Cancel all orders on 'BTC_USDT'
  response = client.orders().cancel(symbol='BTC_USDT')

  # Cancel all orders on 'SPOT' account
  response = client.orders().cancel(account_type='SPOT')
  ```

  - Orders History
  ```python
  # Get a list of historical orders in an account
  response = client.orders().get_history(symbol='BTC_USDT')
  ```

  - Trade History
  ```python
  # Get a list of all trades for an account
  response = client.orders().get_all_trades(limit=5)
  ```

  - Trades by Order Id
  ```python
  # Get a list of all trades for an order specified by its orderId
  response = client.orders().get_trades('21934611974062080')
  ```

  - Kill Switch
  ```python
  # Set a timer that cancels all regular and smartorders after the timeout has expired.
  response = client.orders().set_kill_switch('15')
  ```

  - Kill Switch Status
  ```python
  # Get status of kill switch.
  response = client.orders().get_kill_switch()
  ```

#### Smart Orders
  - Create Order
  ```python
  # Create a smart order for an account (Limit Buy 0.00025 BTC_USDT at 18,000.00 when price hits 20000 USDT)
  response = client.smartorders().create(client_order_id='123Abc',
                                         price='18000',
                                         stop_price='20000.00',
                                         quantity='0.00025',
                                         side='BUY',
                                         symbol='BTC_USDT',
                                         type='LIMIT',
                                         time_in_force='IOC')
  ```

  - Open Orders
  ```python
  # Get a list of (pending) smart orders for an account
  response = client.smartorders().get_all()
  ```

  - Order Details
  ```python
  # Get a smart order’s status. {id} can be smart order’s id or its clientOrderId
  # If smart order’s state is TRIGGERED, the response will include the triggered order’s data

  # Get smart order by client order id
  response = client.smartorders().get_by_id(client_order_id='123Abc')

  # Get smart order by order id
  response = client.smartorders().get_by_id(order_id='21934611974062080')
  ```

  - Cancel Order by Id
  ```python
  # Cancel a smart order by its id

  # Cancel smart order by client order id
  response = client.smartorders().cancel_by_id(client_order_id='123Abc')

  # Cancel smart order by order id
  response = client.smartorders().cancel_by_id(order_id='21934611974062080')
  ```

  - Cancel Multiple Orders by Ids
  ```python
  # Batch cancel one or many active smart orders in an account by IDs
  response = client.smartorders().cancel_by_multiple_ids(
                 order_ids=["12345", "67890"],
                 client_order_ids=["33344", "myId-1"])
  ```

  - Cancel All Orders
  ```python
  # Batch cancel all smart orders in an account

  # Cancel all smart orders on 'BTC_USDT'
  response = client.smartorders().cancel(symbol='BTC_USDT')

  # Cancel all smart orders on 'SPOT' account
  response = client.smartorders().cancel(account_type='SPOT')
  ```

  - Orders History
  ```python
  # Get a list of historical smart orders in an account
  response = client.smartorders().get_history(symbol='BTC_USDT')
  ```

  #### Websockets API

  #### Public Channels
  - Instantiate a client
    ```python
    import asyncio

    from polosdk import WsClientPublic

    def on_message(msg):
        print(msg)

    def on_error(err):
        print(err)

    ws_client_public = WsClientPublic(on_message, on_error=on_error)
    await ws_client_public.connect()
    await ws_client_public.subscribe(['ticker'], ['ETH_USDT'])
    ```

  - Candlesticks
  ```python
  # Continuous feed of candlestick data with default/provided depth
  await ws_client_public.subscribe(['candles_minute_1'], ['BTC_USDT'])
  ```

  - Trades
  ```python
  # Continuous feed of recent trades with default/provided depth
  await ws_client_public.subscribe(['trades'], ['BTC_USDT'])
  ```

  - Ticker
  ```python
  # Continuous feed of current day ticker data
  await ws_client_public.subscribe(['ticker'], ['ETH_USDT'])
  ```

  - Book
  ```python
  # Continuous feed of order book data containing asks and bids with default/provided depth
  await ws_client_public.subscribe(['book'], ['BTC_USDT'])
  # With Depth Parameter
  await ws_client_public.subscribe(['book'], ['BTC_USDT'], depth=10)
  ```

  - Book Level 2
  ```python
  # Receive a snapshot of the full 20 level order book
  # Then, continuously in realtime receive an updated order book when the first 20 levels change
  await ws_client_public.subscribe(['book_lv2'], ['BTC_USDT'])
  ```

  - Subscribing to Multiple Channels
  ```python
  await ws_client_public.subscribe(['book', 'ticker'], ['BTC_USDT'])
  ```

  #### Authenticated Channels
  - Instantiate a client
  ```python
  import asyncio
  import os

  from polosdk import WsClientAuthenticated

  api_key = os.environ['POLO_API_KEY']
  api_secret = os.environ['POLO_API_SECRET']

  def on_message(msg):
      print(msg)

  def on_error(err):
      print(err)

  ws_client_authenticated = WsClientAuthenticated(on_message, on_error=on_error)
  await ws_client_authenticated.connect(api_key, api_secret)
  ```

  - Orders
  ```python
  # Real time information about client’s orders
  await ws_client_authenticated.subscribe(['orders'], ['all'])
  ```

  - Balances
  ```python
  # Real time information about all of client’s balance(s) updates
  await ws_client_authenticated.subscribe(['balances'])
  ```

  - Subscribing to Multiple Channels
  ```python
  await ws_client_authenticated.subscribe(['orders', 'balances'], ['all'])
  ```
