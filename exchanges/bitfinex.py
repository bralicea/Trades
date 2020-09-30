# https://docs.bitfinex.com/docs/ws-general
import base


class Bitfinex(base.Base):
    begin, end = 0, 35

    def onOpen(self):
        for instrument in base.instruments.instruments['bitfinex'][self.begin:self.end]:
            params = {
                'event': 'subscribe',
                'channel': 'trades',
                'symbol': 't{}'.format(instrument)
            }
            subscription = base.json.dumps(params)
            self.sendMessage(subscription.encode('utf8'))

    def onMessage(self, payload, isBinary):
        msg = base.json.loads(payload.decode('utf-8'))
        if isinstance(msg, dict):
            self.producer.send('bitfinexTrades', payload)

        elif isinstance(msg, list) and msg[1] != 'hb':
            self.producer.send('bitfinexTrades', payload)


class Bitfinex35(Bitfinex):
    begin, end = 35, 70

class Bitfinex70(Bitfinex):
    begin, end = 70, 105

class Bitfinex105(Bitfinex):
    begin, end = 105, 140

class Bitfinex140(Bitfinex):
    begin, end = 140, 175

class Bitfinex175(Bitfinex):
    begin, end = 175, 210

class Bitfinex210(Bitfinex):
    begin, end = 210, 245

class Bitfinex245(Bitfinex):
    begin, end = 245, 272


class BitfinexOB(Bitfinex):
    begin, end = 0, 1

    def onOpen(self):
        for instrument in base.instruments.instruments['bitfinex'][self.begin:self.end]:
            params = {
                'event': 'subscribe',
                'channel': 'book',
                'symbol': 't{}'.format(instrument),
                'length': '25'
            }
            subscription = base.json.dumps(params)
            self.sendMessage(subscription.encode('utf8'))

    def onMessage(self, payload, isBinary):
        self.producer.send('bitfinexOrderBooks', payload)


class BitfinexOB35(BitfinexOB):
    begin, end = 35, 70

class BitfinexOB70(BitfinexOB):
    begin, end = 70, 105

class BitfinexOB105(BitfinexOB):
    begin, end = 105, 140

class BitfinexOB140(BitfinexOB):
    begin, end = 140, 175

class BitfinexOB175(BitfinexOB):
    begin, end = 175, 210

class BitfinexOB210(BitfinexOB):
    begin, end = 210, 245

class BitfinexOB245(BitfinexOB):
    begin, end = 245, 272


# Multiple connections to bypass rate limits
base.createConnection("wss://api.bitfinex.com/ws/2", 443, Bitfinex)
base.createConnection("wss://api.bitfinex.com/ws/2", 443, Bitfinex35)
base.createConnection("wss://api.bitfinex.com/ws/2", 443, Bitfinex70)
base.createConnection("wss://api.bitfinex.com/ws/2", 443, Bitfinex105)
base.createConnection("wss://api.bitfinex.com/ws/2", 443, Bitfinex140)
base.createConnection("wss://api.bitfinex.com/ws/2", 443, Bitfinex175)
base.createConnection("wss://api.bitfinex.com/ws/2", 443, Bitfinex210)
base.createConnection("wss://api.bitfinex.com/ws/2", 443, Bitfinex245)

base.createConnection("wss://api.bitfinex.com/ws/2", 443, BitfinexOB)
base.createConnection("wss://api.bitfinex.com/ws/2", 443, BitfinexOB35)
base.createConnection("wss://api.bitfinex.com/ws/2", 443, BitfinexOB70)
base.createConnection("wss://api.bitfinex.com/ws/2", 443, BitfinexOB105)
base.createConnection("wss://api.bitfinex.com/ws/2", 443, BitfinexOB140)
base.createConnection("wss://api.bitfinex.com/ws/2", 443, BitfinexOB175)
base.createConnection("wss://api.bitfinex.com/ws/2", 443, BitfinexOB210)
base.createConnection("wss://api.bitfinex.com/ws/2", 443, BitfinexOB245)

