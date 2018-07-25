import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MarketDataQH.settings')
import django
django.setup()
import datetime
from django.conf import settings
import sys
fn = os.path.join(settings.STATIC_DIR, 'bellport_feeds-20170603.xml')

import xml.etree.ElementTree as ET

from marketdata.models import Feed

class XMLFeedsReader:
    def __init__(self, file=None, ns=None):
        if file is None:
            file = 'bellport_feeds-20170603.xml'
            file = os.path.join(os.environ['MARKET_DATA'], file)

        try:
            tree = ET.parse(file)
            self.root = tree.getroot()
        except:
            self.root = None
            print('exception ******')
        if ns is None:
            self.ns = {'maystreet':
                       'http://www.maystreet.com/SingleFeedSchema.xsd'}
        else:
            self.ns = ns

    def parse(self):
        ns = self.ns
        res = []
        ips = []
        mult = []
        counter = 0
        for feed in self.root.findall('maystreet:Feed', ns):
            feed_name = feed.attrib.get('name') or ''
            feed_type = feed.attrib.get('type') or ''
            end_of_life_date = feed.attrib.get('end_of_life_date') or ''
            for session in feed.findall('maystreet:Session', ns):

                session_name = session.attrib.get('name') or ''

                for connection in session.findall('maystreet:Connection', ns):
                    try:
                        ip_tag = connection.find('maystreet:IPAddress', ns)
                        ip_address = ip_tag.text
                    except:
                        ip_address = ""
                    
                    try:
                        port_tab = connection.find('maystreet:Port', ns)
                        port = port_tab.text
                    except:
                        port = -1

                    try:
                        protocol_tab = connection.find('maystreet:Protocol', ns)
                        protocol = protocol_tab.text
                    except:
                        protocol = ''
                    
                    try:
                        connection_type_tag = connection.find('maystreet:Type', ns)
                        connection_type = connection_type_tag.text
                    except:
                        connection_type = ''

                    try:
                        options = connection.find('maystreet:Options', ns)
                        channel_tag = options.find('maystreet:Channel', ns)
                        channel = channel_tag.text
                    except:
                        channel = ''
                    if end_of_life_date:
                        if datetime.datetime.today() > datetime.datetime.strptime(end_of_life_date, "%Y/%m/%d"):
                            break
                    '''
                    if ip_address == '224.0.130.151' and port == '30031':
                        print("\t".join([feed_name, feed_type, session_name, ip_address, str(port), protocol, connection_type, channel]))
                    '''
                    #res.append(Feed(ip_address, exch, channel))
                    ip = int(ip_address.split('.')[0])
                    if ip >= 224 and ip <= 239:
                        #mult.append("%s:%s%s-%s" %(ip_address, port, feed_name, feed_type))
                        
                        f, created = Feed.objects.get_or_create(
                            multicastGroup = ip_address,
                            port = int(port),
                            protocol = protocol,
                            feedName = feed_name,
                            feedType = feed_type,
                            sessionName = session_name,
                            connectionType = connection_type,
                            channel = channel,
                        )
                        res.append(f)
            
                        if created:
                            print("\t".join([feed_name, feed_type, session_name, ip_address, str(port), protocol, connection_type, channel]))


                    else:
                        #ips.append("%s:%s%s-%s" %(ip_address, port, feed_name, feed_type))
                        ips.append(ip_address)
        '''
        import collections
        print('Mult :%d' %len(mult))
        print('Unic :%d' %len(ips))
        ctr = collections.Counter(mult)
        
        print(len([(c,v) for (c,v) in ctr.items() if v > 1 ]))
        print(len([(c,v) for (c,v) in ctr.items() if v == 1 ]))
        for k,v in ctr.most_common(5):
            print("%16s\t%d" %(k, v))
        '''



if __name__ == '__main__':
    reader = XMLFeedsReader(fn)
    reader.parse()