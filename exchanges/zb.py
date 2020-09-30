import base


class Zb(base.Base):

    def onOpen(self):
        for instrument in base.instruments.instruments['zb']:
            params = {
                "event": "addChannel",
                "channel": "{}_trades".format(instrument)
            }
            subscription = base.json.dumps(params)
            self.sendMessage(subscription.encode('utf8'))

    def onMessage(self, payload, isBinary):
        self.producer.send('zbTrades', payload)


base.createConnection("wss://api.zb.com:9999/websocket", 443, Zb)
