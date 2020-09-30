# https://www.gate.io/docs/websocket/index.html
import base


class Gate(base.Base):

    def sendPingToServer(self):
        if self.state == 3:
            self.sendMessage('{"id":12312, "method":"server.ping", "params":[]}'.encode())

    def onOpen(self):
        params = {
            "id":12312,
            "method": "trades.subscribe",
            "params": base.instruments.instruments['gate']
        }
        subscription = base.json.dumps(params)
        self.sendMessage(subscription.encode('utf8'))

        heartbeat = base.task.LoopingCall(self.sendPingToServer)
        heartbeat.start(60)

    def onMessage(self, payload, isBinary):
        self.producer.send('gateTrades', payload)


base.createConnection("wss://ws.gate.io/v3/", 443, Gate)
