import base


class Poloniex(base.Base):

    def onOpen(self):
        for instrument in base.instruments.instruments['poloniex']:
            params = {
                'command': 'subscribe',
                'channel': '{}'.format(instrument)
            }
            subscription = base.json.dumps(params)
            self.sendMessage(subscription.encode('utf8'))

    def onMessage(self, payload, isBinary):
        self.producer.send('poloniexTrades', payload)


base.createConnection("wss://api2.poloniex.com/", 443, Poloniex)
