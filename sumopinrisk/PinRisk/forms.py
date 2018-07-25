from django import forms
from .models import Trader
import sqlanydb


class RiskParamForm(forms.Form):
    trader = forms.ChoiceField(
        widget=forms.RadioSelect(), 
        choices=[(tdr,tdr) for tdr in Trader.all()]
    )
    #price = forms.DecimalField()
    #percent = forms.DecimalField()
    days = forms.IntegerField()



