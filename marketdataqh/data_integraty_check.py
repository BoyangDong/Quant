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



def check_server_owner():
    for srv in Server.objects.filter(owner_id=None).all():
        print(srv, "**", srv.hostname.split('-')[0].upper())
        try:
            cus = Customer.objects.get(tag=srv.hostname.split('-')[0].upper())
            if cus:
                print("Found Customer:", cus)
                srv.owner = cus
                srv.save()

        except:
            print("NOT FOUND")
        print()
            


def check_server_interface():
    for int_des in InterfaceDescription.objects.filter(server_id=None).all():
        
        srv, created = Server.objects.get_or_create(hostname=int_des.description)
        if created:
            print("Created New Server for", srv.hostname)
        else:
            print("server found")
        int_des.server = srv
        int_des.save()

def link_feed_group():
    for feed in Feed.objects.filter(group_id=None).all():
        #print(feed)
        try:
            group = IGMPSnoopingGroup.objects.get(multicastGroup=feed.multicastGroup)
            
            print("Found:" , group)
        except:
            group = None
            print("NOT FOUND","*%s*" %feed.multicastGroup )
        
        if group:
            feed.group = group
            feed.save()


def fix_feed_ip_space():
    for feed in Feed.objects.all():
        feed.multicastGroup = feed.multicastGroup.strip()
        feed.save()

def fix_igmp_group_ip_space():
    for g in IGMPSnoopingGroup.objects.all():
        g.multicastGroup = g.multicastGroup.strip()

if __name__ == '__main__':
    #fix_feed_ip_space()
    
    #check_server_owner()
    #check_server_interface()
    link_feed_group()