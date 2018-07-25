from django import forms
from  django.forms.widgets import SelectDateWidget
from datetime import datetime as dt
import datetime
YEAR_CHOICES = range(2018, dt.today().year + 2)
MONTHS_CHOICES = {
    1:('JAN'), 2:('FEB'), 3:('MAR'), 4:('APR'),
    5:('MAY'), 6:('JUN'), 7:('JUL'), 8:('AUG'),
    9:('SEP'), 10:('OCT'), 11:('NOV'), 12:('DEC')
}

METHODS = (
    ('1', 'View Here'),
    ('2', 'Download Excel')
)
class YearMonth(forms.Form):
    date = forms.DateField(
        widget=forms.SelectDateWidget(
            years=YEAR_CHOICES, 
            months=MONTHS_CHOICES,
        ),
        initial=datetime.date.today
    )

    display_method = forms.ChoiceField(
        widget=forms.RadioSelect(), 
        choices=METHODS,
        initial=('1', 'View Here'),
        )

    def clean(self):
        all_clean_data = super().clean()
        date = all_clean_data['date']
        #raise forms.ValidationError("Error Message goes here")
        
