# https://biboxcom.github.io/en/ws_api_sub.html#t3
import base


class Bibox(base.Base):

    def onOpen(self):
        for instrument in base.instruments.instruments['bibox']:
            params = {
                "event": "addChannel",
                "channel": "bibox_sub_spot_{}_deals".format(instrument)
            }
            subscription = base.json.dumps(params)
            self.sendMessage(subscription.encode('utf8'))

    def onMessage(self, payload, isBinary):
        self.producer.send('biboxTrades', payload)


class BiboxOB(base.Base):

    def onOpen(self):
        for instrument in base.instruments.instruments['bibox']:
            params = {
                "event": "addChannel",
                "channel": "bibox_sub_spot_{}_depth".format(instrument)
            }
            subscription = base.json.dumps(params)
            self.sendMessage(subscription.encode('utf8'))

    def onMessage(self, payload, isBinary):
        self.producer.send('biboxOrderBooks', payload)


base.createConnection("wss://push.bibox.com/", 443, Bibox)
base.createConnection("wss://push.bibox.com/", 443, BiboxOB)

