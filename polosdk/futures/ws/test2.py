import asyncio

from polosdk.futures.ws.client_authenticated import ClientAuthenticated
from polosdk.futures.ws.client_public import ClientPublic

API_KEY = ''
API_SECRET = ''
ws_public= 'wss://ws.poloniex.com/ws/v3/public'  # 提供给api现货公共频道
ws_private='wss://ws.poloniex.com/ws/v3/private'  # 提供给api+客户端现货私有频道

def on_message(message):
    """处理接收到的消息"""
    if message=={'event': 'pong'}:
        pass
    else:
        print("Received message:", message)

# 处理错误
def on_error(exception):
    """处理发生的错误"""
    # print("Error occurred:", exception)

async def main():
    """主函数，用于初始化 WebSocket 客户端并进行订阅"""
    # 创建公共 WebSocket 客户端
    client = ClientPublic(on_message, ws_url=ws_public)

    # 启动 WebSocket 客户端连接
    await client.connect()

    # 订阅货币信息
    await client.subscribe_to_ProductInfosymbol()

    # 订阅交易信息
    await client.subscribe_to_OrderBook()
    #
    # # 订阅市场深度
    await client.subscribe_to_orderbooklv2()
    #
    # # 订阅 K 线数据
    await client.subscribe_to_KlineData()

    # # 订阅 Ticker 信息
    await client.subscribe_to_IndexPriceKlineData()
    #
    # # 订阅符号信息
    await client.subscribe_to_MarkPriceKlineData()
    await client.subscribe_to_Tickers()
    await client.subscribe_to_Trades()

    await client.subscribe_to_IndexPrice()
    await client.subscribe_to_MarkPrice()
    await client.subscribe_to_FundingRate()

    # 持续监听消息
    try:
        await client.listen()  # 持续监听消息
    except Exception as e:
        print("Error during listening:", e)
    finally:
        # 在完成时断开连接
        await client.disconnect()

async def main2():
    """主函数，用于初始化 WebSocket 客户端并进行私有订阅"""
    # 创建私有 WebSocket 客户端
    client = ClientAuthenticated(on_message, on_error, ws_url=ws_private)

    # 启动 WebSocket 客户端连接
    await client.connect(API_KEY, API_SECRET)
    # await client.subscribe_to_positions()
    # await client.subscribe_to_account()
    await client.subscribe_to_trade()
    # await client.subscribe_to_orders()

    # 持续监听消息
    try:
        await client.listen()  # 持续监听消息
    except Exception as e:
        print("Error during listening:", e)
    finally:
        # 在完成时断开连接
        await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
    asyncio.run(main2())