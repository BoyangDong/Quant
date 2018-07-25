from datetime import datetime as dt
import asyncio
import aiohttp
import json



class StockPrices():
    ''' holds a dictionary of stock symbol and price pairs
    '''
    def __init__(self):
        self.stocks = {}
    
    def download(self, symbols):
        loop = asyncio.SelectorEventLoop()
        asyncio.set_event_loop(loop)

        groups = []
        for i in range(0, len(symbols), 100):
            groups.append(symbols[i:i+100])
        loop.run_until_complete(
            asyncio.gather(
                *(self.async_download_from_alphavantage(','.join(symbols)) for symbols in groups)
            )
        )
        loop.close()
        

    async def async_download_from_alphavantage(self,symbols):
        url = 'https://www.alphavantage.co/query?'\
                'function=BATCH_STOCK_QUOTES&'\
                'symbols=%s&interval=1min&'\
                'apikey=4I3JKSKABXSFCMN9'
        async with aiohttp.ClientSession() as session:
            async with session.get(url % (symbols)) as r:
                data = await r.text()

        try:
            json_result = json.loads(data)
        
            quotes = json_result.get('Stock Quotes')
            for quote in quotes:
                stock = quote.get('1. symbol')
                price = quote.get('2. price')
                self.stocks[stock] = float(price)
        except:
            print("price for:",symbol, "not found")
    def download_one(self, symbol):
        import requests
        url = 'https://www.alphavantage.co/query?'\
              'function=TIME_SERIES_DAILY&'\
              'symbol=%s&apikey=4I3JKSKABXSFCMN9'
        
        r = requests.get(url%symbol)
        try:
            key = r.json().get('Meta Data').get('3. Last Refreshed')
            #key = dt.today().strftime('%Y-%m-%d')
            price = float(r.json().get("Time Series (Daily)")
                                .get(key)
                                .get("4. close"))
        except:
            price = 0
        self.stocks[symbol] = price
        return price

    def get_price(self, symbol):
        return self.stocks.get(symbol) or self.download_one(symbol)
