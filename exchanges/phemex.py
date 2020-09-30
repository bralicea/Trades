import base


class Phemex(base.Base):
    def sendPingToServer(self):
        # Check if websocket connection is open
        if self.state == 3:
            pingMsg = {
              "id": 1234,
              "method": "server.ping",
              "params": []
            }
            self.sendMessage(str(pingMsg).encode())

    def onOpen(self):
        for instrument in base.instruments.instruments['phemex']:
            params = {
              "id": 1234,
              "method": "trade.subscribe",
              "params": [instrument]
            }
            subscription = base.json.dumps(params)
            self.sendMessage(subscription.encode('utf8'))

        heartbeat = base.task.LoopingCall(self.sendPingToServer)
        heartbeat.start(5)

    def onMessage(self, payload, isBinary):
        self.producer.send('phemexTrades', payload)


base.createConnection("wss://phemex.com/ws", 443, Phemex)
