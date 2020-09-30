import base


class Okex(base.Base):

    def onOpen(self):
        params = {
            "op": "subscribe",
            "args": base.instruments.instruments['okex']
        }
        subscription = base.json.dumps(params)
        self.sendMessage(subscription.encode('utf8'))

    def onMessage(self, payload, isBinary):
        self.producer.send('okexTrades', payload)


base.createConnection("wss://real.okex.com:8443/ws/v3", 8443, Okex)
