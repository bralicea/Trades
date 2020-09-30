# https://github.com/coinexcom/coinex_exchange_api/wiki
import base
import sys, os

class CoinEx(base.Base):

    def onOpen(self):
        params = {
          "method": "deals.subscribe",
          "params": base.instruments.instruments['coinex'],
          "id": 16
        }
        subscription = base.json.dumps(params)
        self.sendMessage(subscription.encode('utf8'))

    def onMessage(self, payload, isBinary):
        self.producer.send('coinexTrades', payload)


class CoinExOB(CoinEx):
    ob = {}
    def onOpen(self):
        params0 = {
          "method":"depth.subscribe",
          "params":[
            "BTCUSDT",
            20,
            "0"
          ],
          "id":15
        }
        subscription = base.json.dumps(params0)
        self.sendMessage(subscription.encode('utf8'))

    def onMessage(self, payload, isBinary):
        msg = base.json.loads(payload.decode('utf-8'))
        try:
            if msg['params'][0] == True:
                self.ob[msg['params'][-1]] = {'exchange': 'coinex', 'pair': msg['params'][-1].lower(), 'time': msg['params'][1]['time'], 'bids': [], 'asks': []}
                for bid in msg['params'][1]['bids']:
                    self.ob[msg['params'][-1]]['bids'].append({'price': float(bid[0]), 'amount': float(bid[1])})
                for ask in msg['params'][1]['asks']:
                    self.ob[msg['params'][-1]]['asks'].append({'price': float(ask[0]), 'amount': float(ask[1])})

            else:
                if 'bids' in msg['params'][1]:
                    for bid in msg['params'][1]['bids']:
                        if bid[1] == '0':
                            for cnt, element in enumerate(self.ob[msg['params'][-1]]['bids']):
                                if element['price'] == float(bid[0]):
                                    del self.ob[msg['params'][-1]]['bids'][cnt]
                                    self.ob[msg['params'][-1]]['time'] = msg['params'][1]['time']
                                    break

                        else:
                            for cnt, element in enumerate(self.ob[msg['params'][-1]]['bids']):
                                if element['price'] > float(bid[0]):
                                    self.ob[msg['params'][-1]]['bids'].insert(cnt, {'price': float(bid[0]), 'amount': float(bid[1])})
                                    self.ob[msg['params'][-1]]['time'] = msg['params'][1]['time']
                                    break

                if 'asks' in msg['params'][1]:
                    for ask in msg['params'][1]['asks']:
                        if ask[1] == '0':
                            for cnt, element in enumerate(self.ob[msg['params'][-1]]['asks']):
                                if element['price'] == ask[0]:
                                    del self.ob[msg['params'][-1]]['asks'][cnt]
                                    self.ob[msg['params'][-1]]['time'] = msg['params'][1]['time']
                                    break

                    else:
                        self.ob[msg['params'][-1]]['asks'].append({'price': float(ask[0]), 'amount': float(ask[1])})
                        self.ob[msg['params'][-1]]['time'] = msg['params'][1]['time']

            print(self.ob)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

        #self.producer.send('coinexOrderBooks', payload)

base.createConnection("wss://socket.coinex.com/", 443, CoinEx)
#base.createConnection("wss://socket.coinex.com/", 443, CoinExOB)

#base.reactor.run()
