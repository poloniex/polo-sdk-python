# 假设您的 Accounts 类在 account.py 文件中
# from account import Accounts

# 模拟 API 密钥和秘密
from httpx import patch

from polosdk.spot.rest import client
from polosdk.spot.rest.accounts import Accounts
from polosdk.spot.rest.client import Client
from polosdk.spot.rest.markets import Markets
from polosdk.spot.rest.orders import Orders
from polosdk.spot.rest.smartorders import SmartOrders
from polosdk.spot.rest.subaccounts import Subaccounts
from polosdk.spot.rest.wallets import Wallets

API_KEY = ''
API_SECRET = ''
BASE_URL = 'https://api.poloniex.com'  # 请根据实际情况修改


def main():
    print("开始测试accopunts")
    # 创建 Accounts 实例
    accounts_client = Accounts(api_key=API_KEY, api_secret=API_SECRET, url=BASE_URL)

    # 测试获取所有账户
    try:
        accounts = accounts_client.get_accounts()
        print("Accounts:", accounts)
    except Exception as e:
        print("Error getting accounts:", e)

    # 测试获取账户余额
    try:
        balances = accounts_client.get_balances()
        print("Balances:", balances)
    except Exception as e:
        print("Error getting balances:", e)

    # 测试获取特定账户余额
    if accounts:
        account_id = accounts[0]['accountId']  # 假设我们取第一个账户的ID
        try:
            account_balances = accounts_client.get_account_balances(account_id)
            print(f"Balances for account {account_id}:", account_balances)
        except Exception as e:
            print(f"Error getting balances for account {account_id}:", e)

    # 测试获取费率信息
    try:
        fee_info = accounts_client.get_fee_info()
        print("Fee Information:", fee_info)
    except Exception as e:
        print("Error getting fee information:", e)

    # 测试获取转账记录
    try:
        transfers = accounts_client.get_transfers()
        print("Transfers:", transfers)
    except Exception as e:
        print("Error getting transfers:", e)

    # 测试转账操作（请确保您有足够的资产进行转账）
    # try:
    # transfer_response = accounts_client.transfer('USDT', '10.0', 'SPOT', 'FUTURES')
    # print("Transfer response:", transfer_response)
    # except Exception as e:
    # print("Error during transfer:", e)

    # 测试获取活动记录
    try:
        activities = accounts_client.get_activity()
        print("Activities:", activities)
    except Exception as e:
        print("Error getting activities:", e)

    # 测试获取借款状态
    try:
        borrow_status = accounts_client.get_borrow_status()
        print("Borrow Status:", borrow_status)
    except Exception as e:
        print("Error getting borrow status:", e)

def main2():
    print("开始测试公共API")
    markets_client =Markets( url=BASE_URL)

    # 测试获取特定市场的最新价格
    try:
        price = markets_client.get_price('BTC_USDT')
        print("Latest Price for BTC_USDT:", price)
    except Exception as e:
        print("Error getting price for BTC_USDT:", e)

    # 测试获取所有市场的最新价格
    try:
        prices = markets_client.get_prices()
        print("Latest Prices for all symbols:", prices)
    except Exception as e:
        print("Error getting latest prices for all symbols:", e)

    # 测试获取市场的24小时行情
    try:
        ticker_24h = markets_client.get_ticker24h('BTC_USDT')
        print("24h Ticker for BTC_USDT:", ticker_24h)
    except Exception as e:
        print("Error getting 24h ticker for BTC_USDT:", e)

    # 测试获取所有市场的24小时行情
    try:
        tickers_24h_all = markets_client.get_ticker24h_all()
        print("24h Tickers for all symbols:", tickers_24h_all)
    except Exception as e:
        print("Error getting 24h tickers for all symbols:", e)

    # 测试获取市场的K线数据
    try:
        candles = markets_client.get_candles('BTC_USDT', 'HOUR_1')
        print("Candles for BTC_USDT (1-hour interval):", candles)
    except Exception as e:
        print("Error getting candles for BTC_USDT:", e)

    # 测试获取市场的订单簿
    try:
        orderbook = markets_client.get_orderbook('BTC_USDT')
        print("Order Book for BTC_USDT:", orderbook)
    except Exception as e:
        print("Error getting order book for BTC_USDT:", e)

    # 测试获取市场的最近交易记录
    try:
        trades = markets_client.get_trades('BTC_USDT')
        print("Recent Trades for BTC_USDT:", trades)
    except Exception as e:
        print("Error getting recent trades for BTC_USDT:", e)

    # 测试获取所有交叉保证金的最新标记价格
    try:
        mark_prices = markets_client.get_mark_prices()
        print("Mark Prices for all cross margin symbols:", mark_prices)
    except Exception as e:
        print("Error getting mark prices for all cross margin symbols:", e)

    # 测试获取特定市场的最新标记价格
    try:
        mark_price = markets_client.get_mark_price('BTC_USDT')
        print("Mark Price for BTC_USDT:", mark_price)
    except Exception as e:
        print("Error getting mark price for BTC_USDT:", e)

    # 测试获取某一市场的标记价格组件
    try:
        mark_price_components = markets_client.get_mark_price_components('BTC_USDT')
        print("Mark Price Components for BTC_USDT:", mark_price_components)
    except Exception as e:
        print("Error getting mark price components for BTC_USDT:", e)

    # 测试获取所有货币的抵押信息
    try:
        collateral_info_all = markets_client.get_collateral_info_all()
        print("Collateral Information for all currencies:", collateral_info_all)
    except Exception as e:
        print("Error getting collateral information for all currencies:", e)

    # 测试获取特定货币的抵押信息
    try:
        collateral_info = markets_client.get_collateral_info('BTC')
        print("Collateral Information for BTC:", collateral_info)
    except Exception as e:
        print("Error getting collateral information for BTC:", e)

    # 测试获取所有货币的借款利率信息
    try:
        borrow_rates = markets_client.get_borrow_rates()
        print("Borrow Rates Information:", borrow_rates)
    except Exception as e:
        print("Error getting borrow rates information:", e)

def main3():
    print("开始测试orders")
    # 假设您已经有了 Client 对象
    orders_client = Orders(api_key=API_KEY, api_secret=API_SECRET, url=BASE_URL)


    # 测试创建订单
    try:
        new_order = orders_client.create(
            symbol='BTC_USDT',
            side='BUY',
            quantity='100',
            price='20000',
            type='LIMIT'
        )
        print("New Order Created:", new_order)
    except Exception as e:
        print("Error creating new order:", e)
        # 测试获取所有活动订单
    try:
        active_orders = orders_client.get_all()
        print("Active Orders:", active_orders)
    except Exception as e:
        print("Error getting active orders:", e)

    # 测试获取特定订单信息
    if active_orders:
        order_id = active_orders[0]['id']  # 假设我们取第一个订单的ID
        try:
            order_info = orders_client.get_by_id(order_id=order_id)
            print(f"Order Info for ID {order_id}:", order_info)
        except Exception as e:
            print(f"Error getting order info for ID {order_id}:", e)


    # 测试获取订单历史
    try:
        order_history = orders_client.get_history()
        print("Order History:", order_history)
    except Exception as e:
        print("Error getting order history:", e)

    # 测试获取所有交易记录
    try:
        trades = orders_client.get_all_trades(limit=5)
        print("All Trades:", trades)
    except Exception as e:
        print("Error getting all trades:", e)

    try:
        trades = orders_client.get_trades(order_id=active_orders[0]['id'])
        print("All Trades:", trades)
    except Exception as e:
        print("Error getting all trades:", e)

    # # 测试取消订单
    if active_orders:
        order_id = active_orders[0]['id']  # 假设我们取第一个订单的ID
        try:
            cancel_response = orders_client.cancel_by_id(order_id=order_id)
            print(f"Cancelled Order ID {order_id}:", cancel_response)
        except Exception as e:
            print(f"Error cancelling order ID {order_id}:", e)

    # 测试设置 kill swit ch
    try:
        kill_switch_response = orders_client.set_kill_switch(15)
        print("Kill Switch Set:", kill_switch_response)
    except Exception as e:
        print("Error setting kill switch:", e)

    # 测试获取 kill switch 状态
    try:
        kill_switch_status = orders_client.get_kill_switch()
        print("Kill Switch Status:", kill_switch_status)
    except Exception as e:
        print("Error getting kill switch status:", e)

    # 测试批量创建订单
    try:
        multi_order_request = [
            {
                'symbol': 'BTC_USDT',
                'side': 'BUY',
                'quantity': '100',
                'price': '20000',
                'type': 'LIMIT'
            },
            {
                'symbol': 'ETH_USDT',
                'side': 'SELL',
                'quantity': '100',
                'price': '1500',
                'type': 'LIMIT'
            }
        ]
        batch_order_response = orders_client.create_multiple(multi_order_request)
        print("Batch Orders Created:", batch_order_response)
    except Exception as e:
        print("Error creating batch orders:", e)
    try:
        active_orders = orders_client.get_all()
        print("Active Orders:", active_orders)
    except Exception as e:
        print("Error getting active orders:", e)
    # 测试通过多个 ID 取消订单
    if active_orders:
        order_ids = [order['id'] for order in active_orders[:2]]  # 假设我们取前两个订单的ID
    try:
        cancel_multiple_response = orders_client.cancel_by_multiple_ids(order_ids=order_ids)
        print("Cancelled Multiple Orders:", cancel_multiple_response)
    except Exception as e:
        print("Error cancelling multiple orders:", e)

def main4():
    print("开始测试smartorders")
    # 假设您已经有了 Client 对象
    smart_orders_client =SmartOrders(api_key=API_KEY, api_secret=API_SECRET, url=BASE_URL)



    # 测试创建智能订单
    try:
        new_smart_order = smart_orders_client.create(
            symbol='BTC_USDT',
            side='BUY',
            quantity='0.01',
            stop_price='60000.00',
            price='60100.00',
            type='STOP_LIMIT',
            time_in_force='FOK',
            client_order_id='smartOrder_0011'
        )
        print("New Smart Order Created:", new_smart_order)
    except Exception as e:
        print("Error creating new smart order:", e)

        # 测试获取所有智能订单
    try:
        smart_orders = smart_orders_client.get_all()
        print("All Smart Orders:", smart_orders)
    except Exception as e:
        print("Error getting all smart orders:", e)

    # 测试获取特定智能订单信息
    if smart_orders:
        smart_order_id = smart_orders[0]['id']  # 假设我们取第一个智能订单的ID
        try:
            order_info = smart_orders_client.get_by_id(order_id=smart_order_id)
            print(f"Smart Order Info for ID {smart_order_id}:", order_info)
        except Exception as e:
            print(f"Error getting smart order info for ID {smart_order_id}:", e)

    # 测试取消智能订单
    if smart_orders:
        smart_order_id = smart_orders[0]['id']  # 假设我们取第一个智能订单的ID
        try:
            cancel_response = smart_orders_client.cancel_by_id(order_id=smart_order_id)
            print(f"Cancelled Smart Order ID {smart_order_id}:", cancel_response)
        except Exception as e:
            print(f"Error cancelling smart order ID {smart_order_id}:", e)

    # 测试获取智能订单历史
    try:
        smart_order_history = smart_orders_client.get_history(symbol='BTC_USDT')
        print("Smart Order History:", smart_order_history)
    except Exception as e:
        print("Error getting smart order history:", e)

    # 测试批量取消智能订单
    if smart_orders:
        smart_order_ids = [order['id'] for order in smart_orders[:2]]  # 假设我们取前两个智能订单的ID
        smart_client_order_ids =[order['clientOrderId'] for order in smart_orders[:2]]  # 假设我们取前两个智能订单的ID
        try:
            cancel_multiple_response = smart_orders_client.cancel_by_multiple_ids(order_ids=smart_order_ids,client_order_ids=smart_client_order_ids)
            print("Cancelled Multiple Smart Orders:", cancel_multiple_response)
        except Exception as e:
            print("Error cancelling multiple smart orders:", e)

    # 测试替换智能订单
    if smart_orders:
        smart_order_id = smart_orders[0]['id']  # 假设我们取第一个智能订单的ID
        try:
            replace_response = smart_orders_client.cancel_replace(smart_order_id, price='60500.00',
                                                                  proceed_on_failure=True)
            print(f"Replaced Smart Order ID {smart_order_id}:", replace_response)
        except Exception as e:
            print(f"Error replacing smart order ID {smart_order_id}:", e)

def main5():
    print("开始测试子账户")
    # 假设您已经有了 Client 对象
    subaccounts_client = Subaccounts(api_key=API_KEY, api_secret=API_SECRET, url=BASE_URL)


    # 测试获取所有子账户
    try:
        accounts = subaccounts_client.get_accounts()
        print("Subaccounts:", accounts)
    except Exception as e:
        print("Error getting subaccounts:", e)

    # 测试获取子账户余额
    try:
        balances = subaccounts_client.get_balances()
        print("Subaccount Balances:", balances)
    except Exception as e:
        print("Error getting subaccount balances:", e)

    # 测试获取特定子账户的余额
    if accounts:
        account_id = accounts[0]['accountId']  # 假设我们取第一个子账户的ID
        try:
            account_balances = subaccounts_client.get_account_balances(account_id)
            print(f"Balances for Subaccount {account_id}:", account_balances)
        except Exception as e:
            print(f"Error getting balances for subaccount {account_id}:", e)

    # 测试转账操作（请确保您有足够的资产进行转账）
    if accounts and len(accounts) > 1:
        try:
            transfer_response = subaccounts_client.transfer(
                currency='USDT',
                amount='10',
                from_account_id=accounts[0]['accountId'],
                from_account_type='SPOT',
                to_account_id=accounts[1]['accountId'],
                to_account_type='SPOT'
            )
            print("Transfer Response:", transfer_response)
        except Exception as e:
            print("Error during transfer:", e)

    # 测试获取转账记录
    try:
        transfers = subaccounts_client.get_transfers()
        print("Transfers:", transfers)
    except Exception as e:
        print("Error getting transfers:", e)

    # 测试获取特定转账记录
    if transfers:
        transfer_id = transfers[0]['id']  # 假设我们取第一个转账的ID
        try:
            transfer_info = subaccounts_client.get_transfer(transfer_id)
            print(f"Transfer Info for ID {transfer_id}:", transfer_info)
        except Exception as e:
            print(f"Error getting transfer info for ID {transfer_id}:", e)

def main6():
    print("开始测试钱包")
    # wallets
    # 假设您已经有了 Client 对象
    wallets_client = Wallets(api_key=API_KEY, api_secret=API_SECRET, url=BASE_URL)
    m=Markets(url=BASE_URL)
    k=m.gettimestamp()
    # 测试获取存款地址
    try:
        deposit_addresses = wallets_client.get_deposit_addresses()
        print("Deposit Addresses:", deposit_addresses)
    except Exception as e:
        print("Error getting deposit addresses:", e)

    # 测试获取活动记录
    try:
        activity_history = wallets_client.get_activity(0,end=m.gettimestamp()['serverTime'])
        print("Activity History:", activity_history)
    except Exception as e:
        print("Error getting activity history:", e)

    # 测试创建新的存款地址
    try:
        new_address_response = wallets_client.create_address('TRX')
        print("New Address Created:", new_address_response)
    except Exception as e:
        print("Error creating new deposit address:", e)

    # 测试提取资金
    try:
        withdraw_response = wallets_client.withdraw(
            currency='BTC',
            amount='0.01',  # 请确保此金额在您的余额内
            address='0xbb8d0d7c346daecc2380dabaa91f3ccf8ae232fb4'
        )
        print("Withdrawal Response:", withdraw_response)
    except Exception as e:
        print("Error during withdrawal:", e)

    # 测试提取资金 v2
    try:
        withdraw_v2_response = wallets_client.withdraw_v2(
            coin='BTC',
            network='BTC',
            amount='0.01',  # 请确保此金额在您的余额内
            address='0xbb8d0d7c346daecc2380dabaa91f3ccf8ae232fb4',
        )
        print("Withdrawal v2 Response:", withdraw_v2_response)
    except Exception as e:
        print("Error during v2 withdrawal:", e)
def main7():
    #测试clinet
    c=Client(api_key=API_KEY, api_secret=API_SECRET, url=BASE_URL)
    try:
        deposit_addresses = c.get_timestamp()
        print("Deposit Addresses:", deposit_addresses)
    except Exception as e:
        print("Error getting deposit addresses:", e)

    try:
        deposit_addresses = c.get_markets()
        print("Deposit Addresses:", deposit_addresses)
    except Exception as e:
        print("Error getting deposit addresses:", e)

    try:
        deposit_addresses = c.get_currency(currency="BTC")
        print("Deposit Addresses:", deposit_addresses)
    except Exception as e:
        print("Error getting deposit addresses:", e)

    try:
        account_clinet= c.accounts()
        try:
            accounts = account_clinet.get_accounts()
            print("Accounts:", accounts)
        except Exception as e:
            print("Error getting accounts:", e)
    except Exception as e:
        print("Error getting deposit addresses:", e)


if __name__ == '__main__':
    main()



