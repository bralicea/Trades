#!/usr/bin/python
# /examples/order_book.py

# Sample script showing how order book syncing works.

from __future__ import print_function
from bittrex_websocket import OrderBook
import base
import instruments

producer = base.Base.producer

def main():
    class MySocket(OrderBook):
        def on_ping(self, msg):
            producer.send('bittrexOrderBooks', base.json.dumps(ws.order_books[msg]).encode('utf-8'))


    # Create the socket instance
    ws = MySocket()
    # Enable logging
    ws.enable_log()
    # Define tickers
    tickers = instruments.instruments['bittrex']
    # Subscribe to order book updates
    ws.subscribe_to_orderbook(tickers)

    while True:
        pass
    else:
        pass

if __name__ == "__main__":
    main()
