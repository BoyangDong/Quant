from django.db import models
import sqlanydb
from datetime import datetime as dt
# Create your models here.

class Position:
    def __init__(self, line):
        self.trader = line[0].split(':')[0]
        self.expiration_date = dt.strptime(line[1][10:18], '%Y%m%d')
        self.symbol = ''.join(i for i in line[0].split(':')[1] if not i.isdigit())
        self.positions = int(line[2])
        self.strike_price = float(line[1].split('/')[-1])
        self.call_put = line[1][5]
        self.position_id = int(line[3])
        self.stock_price = 0.0 # set later
        self.percent_diff = 0.0 # set later
        self.price_diff = 0.0 # set later

    def set_price(self, stocks):
        
        self.stock_price = stocks.get_price(self.symbol) or 0.0
        self.price_diff = self.strike_price - self.stock_price
        if self.stock_price != 0:
            self.percent_diff = self.price_diff / self.stock_price


    def __str__(self):
        return "%6s %10s %10s %10s %10s %10s %10s %10s %10s%%" %(
            self.trader, 
            self.expiration_date, 
            self.strike_price, 
            self.symbol,
            self.call_put,
            self.positions,
            self.stock_price,
            self.price_diff,
            self.percent_diff)
       
    def __repr__(self):
        return self.__str__()


    @staticmethod
    def fetch_all():
        #conn = sqlanydb.connect(uid='dba', pwd='dba', eng='AQTOR')
        sql = '''select pf.portfolioName, i.instrumentName, p.position, p.positionId  
                from position as p, instrumentName as i, portfolioName as pf 
                where i.instrumentId = p.instrumentId and p.portfolioId = pf.portfolioId;
            '''
        #cursor = conn.cursor()
        cursor = MyCursor()
        cursor.execute(sql)
        positions = [Position(record) for record in cursor.fetchall() if '/' in record[1]]
        #conn.close()
        return positions
    
    @staticmethod
    def fetch_one(trader):
        #conn = sqlanydb.connect(uid='dba', pwd='dba', eng='AQTOR')
        sql = '''select pf.portfolioName, i.instrumentName, p.position, p.positionId  
                from position as p, instrumentName as i, portfolioName as pf 
                where i.instrumentId = p.instrumentId and p.portfolioId = pf.portfolioId
                and pf.portfolioName like '%s%%';
            ''' % trader
        #cursor = conn.cursor()
        cursor = MyCursor()
        cursor.execute(sql)

        positions = [Position(record) for record in cursor.fetchall() if '/' in record[1]]
   
        #conn.close()
        return positions
        


class Trader():
    def __init__(self, trader):
        self.trader = trader

    def __str__(self):
        return self.trader
    
    def __repr__(self):
        return self.__str__(self)
    
    @staticmethod
    def all():
        #conn = sqlanydb.connect(uid='dba', pwd='dba', eng='AQTOR')
        sql = 'select portfolioName from portfolioName'
        #cursor = conn.cursor()
        cursor = MyCursor()
        cursor.execute(sql)
        traders = [ Trader(tdr) for tdr in set([item[0].split(':')[0] for item in cursor.fetchall() if ':' in item[0]])]
        #conn.close()
        return traders


class Records():
    ''' Records class holds a list of Positions.
        Records instance knows the unique stock symbols of the positions
        Records can filter out Positions with a predicate 
    '''
    def __init__(self, positions):
        self.positions = positions

    def filter(self, pred = lambda _:True):
        # by default, nothing is filtered out
        self.positions = list(filter(pred, self.positions))
    
    def symbols(self):
        return list(set([p.symbol for p in self.positions]))
    

    def set_prices(self, stock):
        ''' stock is a StockPrices object
        '''
        for pos in self.positions:
            pos.set_price(stock)
        

        header = ["Trader","Symbol", "Expiration Date", "Call/Put",
                  "Position", "Stock Price", "Strike Price",
                "Price Diff", "Percent Diff"]
        data = map(lambda x: [x.trader,
                              x.symbol,
                              x.expiration_date.strftime('%m/%d/%Y'),
                              x.call_put,
                              x.positions,
                              "%.2f" %x.stock_price,
                              "%.2f" %x.strike_price,
                              "%.2f" %x.price_diff,
                              "%.2f" %x.percent_diff], self.positions)
        res = [header] + list(data)
        return res

    def get_excel_data(self):
        header = ["Trader","Symbol", "Expiration Date", "Call/Put",
                  "Position", "Stock Price", "Strike Price",
                "Price Diff", "Percent Diff"]
        data = map(lambda x: [x.trader,
                              x.symbol,
                              x.expiration_date.strftime('%m/%d/%Y'),
                              x.call_put,
                              x.positions,
                              "%.2f" %x.stock_price,
                              "%.2f" %x.strike_price,
                              "%.2f" %abs(x.price_diff),
                              "%.2f%%" %(x.percent_diff * 100)], self.positions)
        res = [header] + list(data)
        return res


class MyCursor():
    def __init__(self):
        data =[]

    def execute(self, sql):
      
        import os
        if os.path.isfile('temp.sql'):
            os.remove('temp.sql')
        with open('temp.sql', 'w') as outfile:
            outfile.write(sql)
        
        from subprocess import Popen, PIPE

        cmd = ['dbisql', '-c', 'dsn=QTPortServ', 'temp.sql']
        query = Popen(cmd, stdout=PIPE, stderr=PIPE)
        stdout, stderr = query.communicate()
        lines = str(stdout, 'ascii').split('\r\n')[2:-5]
        self.data = [list(map(lambda x: x.strip(), item.split())) for item in lines]
      


    def fetchall(self):
        return self.data



