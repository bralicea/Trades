import base


class Huobi(base.Base):

    def sendPingToServer(self):
        # Check if websocket connection is open
        if self.state == 3:
            msg = base.json.dumps({'pong': 123})
            self.sendMessage(msg.encode('utf-8'))

    def onOpen(self):
        for instrument in base.instruments.instruments['huobi']:
            msgParams = {
              "sub": "market.{}.trade.detail".format(instrument),
              "id": "id1"
            }
            subscription = base.json.dumps(msgParams)
            self.sendMessage(subscription.encode('utf8'))

        heartbeat = base.task.LoopingCall(self.sendPingToServer)
        heartbeat.start(5)

    def onMessage(self, payload, isBinary):
        self.producer.send('huobiTrades', payload)


base.createConnection("wss://api.huobi.pro/ws", 443, Huobi)
