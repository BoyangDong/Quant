import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MarketDataQH.settings')
import django
django.setup()
from django.conf import settings
from marketdata.models import Customer


customers = """VN,Victory Networks
ACT,accreative
ACTANT,Actant Intelligent Trading
ANDRIE,Andrie Trading
AT,Atlantic Trading Indices, LLC
BT,Benz-Whitehaven
BR,Blackriver
BRE,BRE Trading
Budo,Budo Group, LLC
CT,Cassandra Trading llc
CMZ,CMZ
ES,Edge Specialist
EW,EdgeWater
FI,FlatIron
GB,GBAR
HE,Hard8
KS,Keystone Partners
KOT,Kottke Associates
LTN,LT News
MT,Marathon Trading
MS,MayStreet LLC
MP,MP Capital
ORC,ORC
OIP,Oxford IP
SE,ScriptEdge
SP,Sparta Group
SE-SRV,StateCon
STY,Stuyvesant Trading
SM,Sumo Capital, LLC
SC,Synergy Capital
TM,Third Millenium Trading
TA,Titan Capital
UR,URSA Group, LLC
WB,WhiteBay
ZF,ZenFX
ZT,Zoo Trading
zy,Zydeco
Sumo,Sumo Capital, LLC
MST,MayStreet LLC
WWD,Wildwood Trading, LLC
GrandMasterClock,Victory Networks
ORATS,Victory Networks
CC,C&C
MCM,Monadnock
PROD29,Stuyvesant
RBC,**Terminated**
GS,Geneva Securities
ELK,ELK
"""

def populate():
    for c in customers.split('\n'):
        if c.strip() != "":
            tag, name = c.split(',',1)
            try:
                cus, created = Customer.objects.get_or_create(
                    tag = tag,
                    name = name
                )
                print("created new" if created else "retreived from db")
                print(cus)
            except:
                print('error: %s' %c)

def upper_all():
    for cus in Customer.objects.all():
        cus.tag = cus.tag.upper()
        cus.save()
if __name__ == "__main__":
    upper_all()