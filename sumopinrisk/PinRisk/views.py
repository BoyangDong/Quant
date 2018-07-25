from django.shortcuts import render
from django.http import HttpResponse
import sqlanydb
from . import forms
from .models import Position, Records
from datetime import datetime as dt
from .stockprice import StockPrices
import asyncio
# Create your views here.

    
def index(request):
    if request.method == 'POST':
        form = forms.RiskParamForm(request.POST)
        # set cookie
        if form.is_valid():
            trader = form.cleaned_data['trader']
            #price = form.cleaned_data['price']
            #percent = form.cleaned_data['percent']
            days = form.cleaned_data['days']

            records = Records(Position.fetch_one(trader))
            records.filter(lambda p: abs((p.expiration_date - dt.today()).days) <= days)

            # stocks instance holds a dictionary of stock: price pairs
            stocks = StockPrices()

            # download stock prices for the symbols in record
            stocks.download(records.symbols())

            # set prices and calculate diffs
            records.set_prices(stocks)

            
            #ctx = {'data': records.positions}
            

            #res = render(request, 'display.html', context=ctx)


            from excel_response import ExcelResponse
            res = ExcelResponse(records.get_excel_data(), "PinRiskReport")

            res.set_cookie('trader', trader)
            #res.set_cookie('price', price)
            #res.set_cookie('percent', percent)
            res.set_cookie('days', days)
        
            return res
   
    
    # get cookies 
    trader = request.COOKIES.get('trader')
    #price = request.COOKIES.get('price')
    #percent = request.COOKIES.get('percent')
    days = request.COOKIES.get('days')

    if trader and days:
        # if all cookies are available, use them
        form = forms.RiskParamForm(
            {'trader': trader,
             'days': days }
        )
    else:
        # if not all cookies are available, create default form
        form = forms.RiskParamForm()

    ctx = {'form': form}
    return render(request, 'users.html', context = ctx)


