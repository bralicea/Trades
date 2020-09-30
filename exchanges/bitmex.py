# https://www.bitmex.com/app/wsAPI
import base


class Bitmex(base.Base):

    def onMessage(self, payload, isBinary):
        self.producer.send('bitmexTrades', payload)


class BitmexOB(Bitmex):
    def onMessage(self, payload, isBinary):
        self.producer.send('bitmexOrderBooks', payload)


base.createConnection("wss://www.bitmex.com/realtime?subscribe={}".format(base.instruments.instruments['bitmex']), 443, Bitmex)
base.createConnection("wss://www.bitmex.com/realtime?subscribe={}".format(base.instruments.instruments['bitmexOB']), 443, BitmexOB)
