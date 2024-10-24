import asyncio
import json


# 假设您已经定义了 ClientPublic 和 ClientBase 类

# 处理接收到的消息
from polosdk.spot.ws.client_authenticated import ClientAuthenticated
from polosdk.spot.ws.client_public import ClientPublic

API_KEY = ''
API_SECRET = ''
ws_public= 'wss://ws.poloniex.com/ws/public'  # 提供给api现货公共频道
ws_private='wss://ws.poloniex.com/ws/private'  # 提供给api+客户端现货私有频道


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
    await client.subscribe_to_currencies()

    # 订阅交易信息
    await client.subscribe_to_trades()
    #
    # # 订阅市场深度
    await client.subscribe_to_book()
    #
    # # 订阅 K 线数据
    await client.subscribe_to_candles()

    # # 订阅 Ticker 信息
    await client.subscribe_to_ticker()
    #
    # # 订阅符号信息
    await client.subscribe_to_symbols()
    await client.subscribe_to_booklv2()
    await client.subscribe_to_exchange()

    # 持续监听消息
    try:
        await client.listen()  # 持续监听消息
    except Exception as e:
        print("Error during listening:", e)
    finally:
        # 在完成时断开连接
        await client.disconnect()

async def main2():
    client = ClientAuthenticated(on_message, ws_url=ws_private,on_error=on_error)

    # 启动 WebSocket 客户端连接
    await client.connect(api_key=API_KEY, api_secret=API_SECRET)

    await client.subscribe_to_orders()
    await client.subscribe_to_createorder()
    await client.subscribe_to_balances()
    await client.subscribe_to_cancelmultipleorders()
    await client.subscribe_to_cancelall()

    # 持续监听消息
    try:
        await client.listen()  # 持续监听消息
    except Exception as e:
        print("Error during listening:", e)
    finally:
        # 在完成时断开连接
        await client.disconnect()


if __name__ == '__main__':
    asyncio.run(main2())