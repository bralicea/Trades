# https://docs.gemini.com/websocket-api/
import base
import instruments


class Gemini(base.Base):

    def onOpen(self):
        params = '{"type": "subscribe","subscriptions":[{"name":"l2","symbols":' + (instruments.instruments['gemini']) + '}]}'
        self.sendMessage(params.encode('utf8'))

    def onMessage(self, payload, isBinary):
        payload = base.json.loads(payload.decode('utf-8'))
        if payload['type'] == 'trade':
            self.producer.send('geminiTrades', base.json.dumps(payload).encode('utf-8'))


base.createConnection("wss://api.gemini.com/v2/marketdata", 443, Gemini)
