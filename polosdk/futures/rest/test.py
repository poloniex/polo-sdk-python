from polosdk.futures.rest.private import Private
from polosdk.futures.rest.public import Public
#
API_KEY=""
SECRET=""
HOST = 'https://api.poloniex.com'  # 请根据实际情况修改

def main():
    # 创建 Public 实例
    public_client = Public(url=HOST)
    # 1. 获取订单簿
    try:
        order_book = public_client.get_order_book('BTC_USDT')
        print("Order Book:", order_book)
    except Exception as e:
        print("Error getting order book:", e)

    # 2. 获取 K 线数据
    try:
        k_line_data = public_client.get_k_line_data("BTC_USDT_PERP", 'MINUTE_1')
        print("K Line Data:", k_line_data)
    except Exception as e:
        print("Error getting K line data:", e)

    # 3. 获取执行信息
    try:
        execution_info = public_client.get_execution_info("BTC_USDT_PERP")
        print("Execution Info:", execution_info)
    except Exception as e:
        print("Error getting execution info:", e)

    # 4. 获取市场信息
    try:
        market_info = public_client.get_narket_info()
        print("Market Info:", market_info)
    except Exception as e:
        print("Error getting market info:", e)

    # 5. 获取指数价格
    try:
        index_price = public_client.index_price()
        print("Index Price:", index_price)
    except Exception as e:
        print("Error getting index price:", e)

    # 6. 获取指数价格成分
    try:
        index_price_components = public_client.get_index_price_components("BTC_USDT_PERP")
        print("Index Price Components:", index_price_components)
    except Exception as e:
        print("Error getting index price components:", e)

    # 7. 获取指数价格 K 线数据
    try:
        index_price_k_line_data = public_client.get_index_price_k_line_data("BTC_USDT_PERP", 'MINUTE_1')
        print("Index Price K Line Data:", index_price_k_line_data)
    except Exception as e:
        print("Error getting index price K line data:", e)

    # 8. 获取标记价格
    try:
        mark_price = public_client.get_mark_price()
        print("Mark Price:", mark_price)
    except Exception as e:
        print("Error getting mark price:", e)

    # 9. 获取标记价格 K 线数据
    try:
        mark_price_k_line_data = public_client.get_mark_price_k_line_data("BTC_USDT_PERP", 'MINUTE_1')
        print("Mark Price K Line Data:", mark_price_k_line_data)
    except Exception as e:
        print("Error getting mark price K line data:", e)

    try:
        pre_price_k_line_data = public_client.get_premium_index_price_k_line_data("BTC_USDT_PERP", 'MINUTE_1')
        print("Premium Price K Line Data:",  pre_price_k_line_data)
    except Exception as e:
        print("Error getting premium price K line data:", e)

    # 10. 获取产品信息
    try:
        product_info = public_client.get_product_info("BTC_USDT_PERP")
        print("Product Info:", product_info)
    except Exception as e:
        print("Error getting product info:", e)

    # 11. 获取当前融资利率
    try:
        current_funding_rate = public_client.get_current_funding_rate("BTC_USDT_PERP")
        print("Current Funding Rate:", current_funding_rate)
    except Exception as e:
        print("Error getting current funding rate:", e)

    # 12. 获取历史融资利率
    try:
        history_funding_rate = public_client.get_history_funding_rate(symbol="BTC_USDT_PERP")
        print("History Funding Rate:", history_funding_rate)
    except Exception as e:
        print("Error getting history funding rate:", e)

    # 13. 获取当前未平仓合约
    try:
        current_open_positions = public_client.get_current_open_positions("BTC_USDT_PERP")
        print("Current Open Positions:", current_open_positions)
    except Exception as e:
        print("Error getting current open positions:", e)

    # 14. 获取保险基金信息
    try:
        insurance_fund_info = public_client.get_query_insurance_fund_information()
        print("Insurance Fund Information:", insurance_fund_info)
    except Exception as e:
        print("Error getting insurance fund information:", e)

    # 15. 获取期货风险限制
    try:
        futures_risk_limit = public_client.get_futures_risk_limit()
        print("Futures Risk Limit:", futures_risk_limit)
    except Exception as e:
        print("Error getting futures risk limit:", e)

def main2():
    # 创建 Private 实例
    private_client = Private(api_key=API_KEY, api_secret=SECRET, url=HOST)

    try:
        account_balance = private_client.get_account_balance()
        print("Account Balance:", account_balance)
    except Exception as e:
        print("Error getting account balance:", e)

        # 2. 测试下单
    try:
        order_response = private_client.place_order("BTC_USDT_PERP", 'BUY', 'LIMIT', '1', px='50')
        print("Place Order Response:", order_response)
    except Exception as e:
        print("Error placing order:", e)

        # 3. 测试下多个订单
    orders = [
        {
            "symbol": "BTC_USDT_PERP",
            "side": "SELL",
            "type": "MARKET",
            "px": "60",
            "sz": "1",
            "timeInForce": "GTC",
            "stpMode": "",
            "reduceOnly": False,
            "clOrdId": "310d7fc9-8bb4-472f-b477-d974724f077d"
        },
        {
            "symbol": "BTC_USDT_PERP",
            "side": "BUY",
            "type": "MARKET",
            "px": "60",
            "sz": "2",
            "timeInForce": "GTC",
            "stpMode": "EXPIRE_TAKER",
            "reduceOnly": False,
            "clOrdId": "2486353f-64d3-4f7d-aa0a-7e34f45b6a6e"
        },
        # 其他订单...
    ]

    try:
        response = private_client.place_multiple_orders(orders)
        print("Place Multiple Orders Response:", response)
    except Exception as e:
        print("Error placing multiple orders:", e)

        # 4. 测试取消订单
    try:
        cancel_response = private_client.cancel_order("BTC_USDT_PERP",ordId=order_response['data']['ordId'])  # 替换为实际的订单ID
        print("Cancel Order Response:", cancel_response)
    except Exception as e:
        print("Error canceling order:", e)

       # 5. 测试取消多个订单
    try:
        cancel_multiple_response = private_client.cancel_multiple_order("BTC_USDT_PERP",clOrdIds=[order_response['data']['clOrdId']])  # 替换为实际的订单ID
        print("Cancel Multiple Orders Response:", cancel_multiple_response)
    except Exception as e:
        print("Error canceling multiple orders:", e)

    try:
        cancel_multiple_response = private_client.cancel_all_order()  # 替换为实际的订单ID
        print("Cancel All Orders Response:", cancel_multiple_response)
    except Exception as e:
        print("Error canceling All orders:", e)

        # 6. 测试平仓（市价）
    try:
        close_response = private_client.close_at_market_price("BTC_USDT_PERP")
        print("Close at Market Price Response:", close_response)
    except Exception as e:
        print("Error closing at market price:", e)

        # 7. 测试平仓所有头寸
    try:
        close_all_response = private_client.close_all_at_market_price()
        print("Close All at Market Price Response:", close_all_response)
    except Exception as e:
        print("Error closing all at market price:", e)

        # 8. 测试获取当前订单
    try:
        current_orders = private_client.get_current_orders()
        print("Current Orders:", current_orders)
    except Exception as e:
        print("Error getting current orders:", e)

        # 9. 测试获取执行详情
    try:
        execution_details = private_client.get_execution_details()
        print("Execution Details:", execution_details)
    except Exception as e:
        print("Error getting execution details:", e)

        # 10. 测试获取订单历史
    try:
        order_history = private_client.get_order_history()
        print("Order History:", order_history)
    except Exception as e:
        print("Error getting order history:", e)

        # 11. 测试获取当前头寸
    try:
        current_position = private_client.get_current_position()
        print("Current Position:", current_position)
    except Exception as e:
        print("Error getting current position:", e)

        # 12. 测试获取头寸历史
    try:
        position_history = private_client.get_position_history(symbol="BTC_USDT_PERP")
        print("Position History:", position_history)
    except Exception as e:
        print("Error getting position history:", e)

        # 13. 测试调整保证金
    try:
        adjust_margin_response = private_client.adjust_margin("BTC_USDT_PERP",type="ADD",amt="50")  # 替换为实际的金额和类型
        print("Adjust Margin Response:", adjust_margin_response)
    except Exception as e:
        print("Error adjusting margin:", e)

        # 14. 测试切换保证金模式
    try:
        switch_response = private_client.switch_cross("BTC_USDT_PERP","CROSS")  # 替换为实际的保证金模式
        print("Switch Margin Mode Response:", switch_response)
    except Exception as e:
        print("Error switching margin mode:", e)

        # 15. 测试获取保证金模式
    try:
        margin_mode = private_client.get_margin_mode("BTC_USDT_PERP")
        print("Margin Mode:", margin_mode)
    except Exception as e:
        print("Error getting margin mode:", e)

        # 16. 测试获取杠杆
    try:
        leverage = private_client.get_leverge("BTC_USDT_PERP")
        print("Leverage:", leverage)
    except Exception as e:
        print("Error getting leverage:", e)

        # 17. 测试设置杠杆
    try:
        set_leverage_response = private_client.set_leverge("BTC_USDT_PERP", '10')  # 替换为实际的杠杆值
        print("Set Leverage Response:", set_leverage_response)
    except Exception as e:
        print("Error setting leverage:", e)

if __name__ == '__main__':
    main()
