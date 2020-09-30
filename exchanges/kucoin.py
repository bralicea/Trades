import base


class Kucoin(base.Base):

    start, end = 0, 99

    def sendPingToServer(self):
        # Check if websocket connection is open
        if self.state == 3:
            pingMsg = base.json.dumps({
              "id": 1545910660739,
              "type": "ping"
            })
            self.sendMessage(pingMsg.encode('utf-8'))

    def onOpen(self):
        for instrument in base.instruments.instruments['kucoin'][self.start:self.end]:
            params = {
                "id": 1545910660739,
                "type": "subscribe",
                "topic": "/market/match:{}".format(instrument),
                "response": True
            }
            subscription = base.json.dumps(params)
            self.sendMessage(subscription.encode('utf8'))

        heartbeat = base.task.LoopingCall(self.sendPingToServer)
        heartbeat.start(50)

    def onMessage(self, payload, isBinary):
        self.producer.send('kucoinTrades', payload)

class Kucoin100(Kucoin):

    start, end = 99, 198

class Kucoin200(Kucoin):

    start, end = 198, 297

class Kucoin300(Kucoin):

    start, end = 297, 396

class Kucoin400(Kucoin):

    start, end = 396, 430


# Request token to establish websocket connection
getToken = base.json.loads((base.requests.post('https://api.kucoin.com/api/v1/bullet-public').content).decode('utf-8'))
base.createConnection("wss://push-private.kucoin.com/endpoint?token={}".format(getToken['data']['token']), 443, Kucoin)
base.createConnection("wss://push-private.kucoin.com/endpoint?token={}".format(getToken['data']['token']), 443, Kucoin100)
base.createConnection("wss://push-private.kucoin.com/endpoint?token={}".format(getToken['data']['token']), 443, Kucoin200)
base.createConnection("wss://push-private.kucoin.com/endpoint?token={}".format(getToken['data']['token']), 443, Kucoin300)
base.createConnection("wss://push-private.kucoin.com/endpoint?token={}".format(getToken['data']['token']), 443, Kucoin400)
