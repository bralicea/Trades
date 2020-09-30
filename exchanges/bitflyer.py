# https://bf-lightning-api.readme.io/docs?ljs=en
import base


class Bitflyer(base.Base):

    def onOpen(self):
        for instrument in base.instruments.instruments['bitflyer']:
            msgParams = {
                "method": "subscribe",
                "params": {
                    "channel": 'lightning_executions_{}'.format(instrument)
                }
            }
            subscription = base.json.dumps(msgParams)
            self.sendMessage(subscription.encode('utf8'))

    def onMessage(self, payload, isBinary):
        self.producer.send('bitflyerTrades', payload)


class BitflyerOB(Bitflyer):

    def onOpen(self):
        for instrument in base.instruments.instruments['bitflyer']:
            msgParams = {
                "method": "subscribe",
                "params": {
                    "channel": 'lightning_board_snapshot_{}'.format(instrument)
                }
            }
            subscription = base.json.dumps(msgParams)
            self.sendMessage(subscription.encode('utf8'))

    def onMessage(self, payload, isBinary):
        self.producer.send('bitflyerOrderBooks', payload)


base.createConnection("wss://ws.lightstream.bitflyer.com/json-rpc", 443, Bitflyer)
base.createConnection("wss://ws.lightstream.bitflyer.com/json-rpc", 443, BitflyerOB)
