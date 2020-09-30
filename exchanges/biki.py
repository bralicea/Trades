# https://github.com/code-biki/open-api/blob/master/README.us-en.md
import base


class Biki(base.Base):

    def onOpen(self):
        for instrument in base.instruments.instruments['biki']:
            params = {
                "event": "sub",
                "params": {
                    "channel": "market_{}_trade_ticker".format(instrument),
                    "cb_id": "Customer"
                }
            }
            subscription = base.json.dumps(params)
            self.sendMessage(subscription.encode('utf8'))

    def onMessage(self, payload, isBinary):
        self.producer.send('bikiTrades', payload)


class BikiOB(Biki):

    def onOpen(self):
        for instrument in base.instruments.instruments['biki']:
            params = {
                "event": "sub",
                "params": {
                    "channel": "market_{}_depth_step1".format(instrument),
                    "cb_id": "Customer"
                }
            }
            subscription = base.json.dumps(params)
            self.sendMessage(subscription.encode('utf8'))

    def onMessage(self, payload, isBinary):
        self.producer.send('bikiOrderBooks', payload)


base.createConnection("wss://ws.biki.com/kline-api/ws", 443, Biki)
base.createConnection("wss://ws.biki.com/kline-api/ws", 443, BikiOB)
