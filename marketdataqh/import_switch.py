import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MarketDataQH.settings')
import django
django.setup()
from django.conf import settings
from marketdata.models import Switch


switches = """
arista,10.64.254.1
arista,10.10.128.3
arista,10.64.254.2
arista,10.75.128.9
arista,10.10.129.1
arista,10.10.129.2
arista,10.66.254.5
arista,10.75.128.10
arista,10.75.128.4
arista,10.75.128.11
arista,10.64.254.6
arista,10.64.254.5
catalyst,10.10.4.6
catalyst,10.10.129.3
nexus,10.63.254.1
nexus,10.10.0.2
nexus,10.62.254.2
nexus,10.10.4.200
nexus,10.10.4.201
nexus,10.13.128.1
nexus,10.10.128.1
nexus,10.10.4.4
nexus,10.62.254.2
"""


if __name__ == "__main__":
    for l in switches.split('\n'):
        if l.strip() != "":
            model, ip = l.split(',')
            try:
                sw, created = Switch.objects.get_or_create(
                    ip = ip,
                    model = model
                )
                print("created new" if created else "retrived from db")
                print(sw)
            except:
                print("error: %s" %l)