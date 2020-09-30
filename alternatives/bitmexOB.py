        try:
            if 'action' in msg:
                if msg['action'] == 'partial':
                    OB[msg["filter"]["symbol"]] = {"exchange": "bitmex", "pair": msg["filter"]["symbol"].lower(), "time": time.time_ns() // 1000000, "bids": [], "asks": []}
                    for entry in msg['data']:
                        OBid["id"] = entry["price"]
                        if entry['side'] == 'Buy':
                            OB[msg["filter"]["symbol"]]['bids'].append({'price': float(entry['price']), 'amount': float(entry['size'])})

                        elif entry['side'] == 'Sell':
                            OB[msg["filter"]["symbol"]]['asks'].append({'price': float(entry['price']), 'amount': float(entry['size'])})

                    OB[msg["filter"]["symbol"]]['asks'] = OB[msg["filter"]["symbol"]]['asks'][::-1]

                    await orderbooks.send(value=OB[msg['filter']['symbol']])

                elif msg['action'] == 'update':
                    for entry in msg['data']:
                        if entry['side'] == 'Sell':
                            for count, ask in enumerate(OB[entry['symbol']]['asks']):
                                if ask['price'] == OBid[entry['id']]:
                                    OB[entry['symbol']]['asks'][count]['amount'] = float(entry['size'])
                                    OB[entry['symbol']]['time'] = time.time_ns() // 1000000
                                    break

                        elif entry['side'] == 'Buy':
                            for count, bid in enumerate(OB[entry['symbol']]['bids']):
                                if bid['price'] == OBid[entry['id']]:
                                    OB[entry['symbol']]['bids'][count]['amount'] = float(entry['size'])
                                    OB[entry['symbol']]['time'] = time.time_ns() // 1000000
                                    break

                    await orderbooks.send(value=OB[msg['data'][0]['symbol']])

                elif msg['action'] == 'insert':
                    for entry in msg['data']:
                        OBid[entry['id']] = entry['price']
                        if entry['side'] == 'Sell':
                            for cnt, ask in enumerate(OB[entry['symbol']]['asks']):
                                if float(entry['price']) < ask['price']:
                                    OB[entry['symbol']]['asks'].insert(cnt, {'price': float(entry['price']), 'amount': float(entry['size'])})
                                    OB[entry['symbol']]['time'] = time.time_ns() // 1000000
                                    break

                        elif entry['side'] == 'Buy':
                            for cnt, bid in enumerate(OB[entry['symbol']]['bids']):
                                if float(entry['price']) < bid['price']:
                                    OB[entry['symbol']]['bids'].insert(cnt, {'price': float(entry['price']), 'amount': float(entry['size'])})
                                    OB[entry['symbol']]['time'] = time.time_ns() // 1000000
                                    break

                    await orderbooks.send(value=OB[msg['data'][0]['symbol']])

                elif msg['action'] == 'delete':
                    for entry in msg['data']:
                        if entry['id'] in OBid:
                            if entry['side'] == 'Sell':
                                for count, ask in enumerate(OB[entry['symbol']]['asks']):
                                    if ask['price'] == OBid[entry['id']]:
                                        del OB[entry['symbol']]['asks'][count]
                                        del OBid[entry['id']]
                                        OB[entry['symbol']]['time'] = time.time_ns() // 1000000
                                        break

                            elif entry['side'] == 'Buy':
                                for count, bid in enumerate(OB[entry['symbol']]['bids']):
                                    if bid['price'] == OBid[entry['id']]:
                                        del OB[entry['symbol']]['bids'][count]
                                        del OBid[entry['id']]
                                        OB[entry['symbol']]['time'] = time.time_ns() // 1000000
                                        break

                    await orderbooks.send(value=OB[msg['data'][0]['symbol']])
