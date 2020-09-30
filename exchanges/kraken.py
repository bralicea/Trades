import base


class Kraken(base.Base):
    def onOpen(self):
        params = {
          "event": "subscribe",
          "pair": base.instruments.instruments['kraken'],
          "subscription": {
            "name": "trade"
          }
        }
        subscription = base.json.dumps(params)
        self.sendMessage(subscription.encode('utf8'))

    def onMessage(self, payload, isBinary):
        self.producer.send('krakenTrades', payload)


base.createConnection("wss://ws.kraken.com", 443, Kraken)
