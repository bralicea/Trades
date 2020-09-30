# https://docs.pro.coinbase.com/#websocket-feed
import base


class Coinbase(base.Base):
    def onOpen(self):
        for instrument in base.instruments.instruments['coinbase']:
            params = {
                "type": "subscribe",
                "channels": [{"name": "matches", "product_ids": [instrument]}]
            }
            subscription = base.json.dumps(params)
            self.sendMessage(subscription.encode('utf8'))

    def onMessage(self, payload, isBinary):
        self.producer.send('coinbaseTrades', payload)

base.createConnection("wss://ws-feed.pro.coinbase.com", 443, Coinbase)
