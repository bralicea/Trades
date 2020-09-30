# https://www.bitstamp.net/websocket/v2/
import base


class Bitstamp(base.Base):

    def onOpen(self):
        for instrument in base.instruments.instruments['bitstamp']:
            params = {
                'event': 'bts:subscribe',
                'data': {
                    'channel': 'live_trades_{}'.format(instrument)
                }
            }
            subscription = base.json.dumps(params)
            self.sendMessage(subscription.encode('utf8'))

    def onMessage(self, payload, isBinary):
        self.producer.send('bitstampTrades', payload)


class BitstampOB(Bitstamp):

    def onOpen(self):
        for instrument in base.instruments.instruments['bitstamp']:
            params = {
                'event': 'bts:subscribe',
                'data': {
                    'channel': 'order_book_{}'.format(instrument)
                }
            }
            subscription = base.json.dumps(params)
            self.sendMessage(subscription.encode('utf8'))

    def onMessage(self, payload, isBinary):
        self.producer.send('bitstampOrderBooks', payload)

base.createConnection("wss://ws.bitstamp.net", 443, Bitstamp)
base.createConnection("wss://ws.bitstamp.net", 443, BitstampOB)
