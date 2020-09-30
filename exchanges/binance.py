# https://github.com/binance-exchange/binance-official-api-docs/blob/master/web-socket-streams.md
import base


class Binance(base.Base):

    def onMessage(self, payload, isBinary):
        self.producer.send('binanceTrades', payload)


class BinanceOB(Binance):

    def onMessage(self, payload, isBinary):
        self.producer.send('binanceOrderBooks', payload)


base.createConnection("wss://stream.binance.com:9443/stream?streams={}".format(base.instruments.instruments['binance']), 9443, Binance)
base.createConnection("wss://stream.binance.com:9443/stream?streams={}".format(base.instruments.instruments['binanceOB']), 9443, BinanceOB)
