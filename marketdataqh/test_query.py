import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MarketDataQH.settings')
import django
django.setup()
from django.conf import settings
import paramiko
import sys
import atexit
import re
from datetime import datetime as dt
from marketdata.models import * 
from marketdata.view_healpers import AccessRecordFinder




def test_customer():
    cus = Customer.objects.get(tag='233')
    print(cus)

def test_prefetch():
    counter = 0
    for ar in AccessRecord.objects.prefetch_related('interface__server__owner', 'multicastGroup__feed_set').all()[:10]:
        group = ar.multicastGroup.multicastGroup
        interface = ar.interface.interface
        for feed in ar.multicastGroup.feed_set.all():
            print(group, interface, feed)

def test_generator():
    arf = AccessRecordFinder("2018", "04")
    for l in arf:
        print(l)
if __name__ == '__main__':
    #test_customer()
    #test_prefetch()
    #test_generator()
