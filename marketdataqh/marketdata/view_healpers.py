from marketdata.models import * 


class AccessRecordFinder():
    def __init__(self, year, month):
        self.records = AccessRecord.objects.prefetch_related(
            'interface__server__owner', 
            'multicastGroup__feed_set').filter(year=str(year), month=str(month).zfill(2))
        
    
    def __iter__(self):
        for record in self.records:
            interface_obj = record.interface
            group = record.multicastGroup.multicastGroup 
            status = interface_obj.status or ""

            switch_ip = interface_obj.switchIP
            interface = interface_obj.interface
            description = interface_obj.description
            try:
                customer = interface_obj.server.owner.name
            except:
                customer = ""
            
            if record.multicastGroup.feed_set.exists():
                for feed in record.multicastGroup.feed_set.all():
                    port = str(feed.port) or ""
                    protocol = feed.protocol or ""
                    channel = feed.channel or ""
                    feedName = feed.feedName or ""
                    feedType = feed.feedType or ""
                    sessionName = feed.sessionName or ""
                    yield [
                        description,
                        feedName,
                        feedType,
                        sessionName,
                        group,
                        port,
                        channel,
                        protocol,
                        customer,
                        interface,
                        status,
                        switch_ip
                    ]
            else:
                yield [
                        description,
                        "",
                        "",
                        "",
                        group,
                        "",
                        "",
                        protocol,
                        customer,
                        interface,
                        status,
                        switch_ip
                ]


    def get_excel_data(self):
        header = [
            'Description',
            'Feed Name',
            'Feed Type',
            'Session Name',
            'Multicast Group',	
            'Port',	
            'Channel',	
            'Protocol',	
            'Customer',	
            'Switch Interface',	
            'Status',	
            'Switch IP'
        ]
        return [header] + list(self.__iter__())

            
            
