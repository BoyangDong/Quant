from django.shortcuts import render
from marketdata.models import *
from . import forms
# Create your views here.



def index(request):
    return render(request, 'base.html', context={})



def display(request):
    my_dict = {'records': AccessRecord.objects.prefetch_related('interface__server__owner', 'multicastGroup__feed_set').all()}
    return render(request, 'display.html', context=my_dict)


def year_month_form(request):
    form = forms.YearMonth()

    if request.method == 'POST':
        form = forms.YearMonth(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            year = date.year
            month = date.month
            from .view_healpers import AccessRecordFinder
            
            arf = AccessRecordFinder(year,month)
            option = form.cleaned_data['display_method']
            if option == '1':
                return render(request, 'display.html', context={'records': arf})
            else: # == '2'
                from excel_response import ExcelResponse
                return ExcelResponse(arf.get_excel_data(), "MarketDataReport_%s_%s" %(year, month))


    return render(request, 'year_month.html', context={'form': form})