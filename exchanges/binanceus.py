# https://github.com/binance-us/binance-official-api-docs/blob/master/web-socket-streams.md
import base


class BinanceUs(base.Base):

    def onMessage(self, payload, isBinary):
        self.producer.send('binanceUsTrades', payload)


class BinanceUsOB(base.Base):

    def onMessage(self, payload, isBinary):
        self.producer.send('binanceUsOrderBooks', payload)


base.createConnection("wss://stream.binance.us:9443/stream?streams={}".format(base.instruments.instruments['binanceus']), 9443, BinanceUs)
base.createConnection("wss://stream.binance.us:9443/stream?streams={}".format(base.instruments.instruments['binanceusOB']), 9443, BinanceUsOB)
