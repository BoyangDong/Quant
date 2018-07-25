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
import traceback

class SSHClient():
    ''' SSHClient takes a switch object, uses its ip to start ssh connection
        then runs the _basic_cmd to enter the privileged exec mode, then
        the ssh client does one thing only -- to send_command an return output
    '''
    def __init__(self, sw):
        print(sw)
        self.swip = sw.ip
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(sw.ip, username=settings.SWUSER, password=settings.SWPW,
                                allow_agent=False, look_for_keys=False)
        except:
            try:
                self.client.close()
            except:
                print("failed to close")
                print('exiting...')
                sys.exit(1)
            print("unable to connect, moving on to next")
            self.client = None

        def _close():
            self.client.close()
        if self.client: 
            atexit.register(_close)
            self._basic_cmd()

    def send_command(self, cmd):
        if not self.client:
            return
        print("SEND COMMAND: %s" %cmd)
        return self._exec(cmd)

    def _exec(self, cmd):
        if not self.client:
            return
        if self.client:
            try:
                stdin, stdout, stderr = self.client.exec_command(cmd)
                
            except:
                self.client.connect(self.swip, username=settings.SWUSER, password=settings.SWPW,
                                    allow_agent=False, look_for_keys=False)
                stdin, stdout, stderr = self.client.exec_command(cmd)
            alldata = b""
            while not stdout.channel.exit_status_ready():
                if stdout.channel.recv_ready():
                    alldata += stdout.channel.recv(1024)
                    newdata = b"1"
                    while stdout.channel.recv_ready():
                        newdata = stdout.channel.recv(1024)
                        alldata += newdata
            try:
                return str(alldata, 'utf8')
            except:
                return None       
    def _basic_cmd(self):
        ''' run this everytime to enter privileged exec mode
            and set terminal length to 0 to disable pagination
        '''
        #self._exec('enable')
        #self._exec(settings.SWPW)
        self._exec('terminal length 0')


class InterfaceDescriptionParser():
    def parse(self, raw):
        pass
    
    def parse_from_shell(self, ssh):
        return self.parse(ssh.send_command(self.cmd))


class AristaIntDesParser(InterfaceDescriptionParser):
    def __init__(self):
        self.cmd = 'show interface description'

    def parse(self, raw):
        if not raw:
            return {}
        res = {}
        content = [l for l in raw.split('\n')[1:-1] if l.strip() != ""]
        for line in content:
            l = line.split()
            if len(l) < 4:
                interface = line[:28].strip()
                status = line[28:40].strip()
                protocol = line[40:].strip()
                description = ""
            else:
                interface = l[0].strip()
                status = l[1].strip()
                protocol = l[2].strip()
                description = " ".join(l[3:]).strip()
            res[interface] = (description, status, protocol, line)
        return res

class CatalystDesParser(InterfaceDescriptionParser):
    def __init__(self):
        self.cmd = 'show interface description'

    def parse(self, raw):
        if not raw:
            return {}
        res = {}
        content = [l for l in raw.split('\n')[2:] if l.strip() != ""]

        for line in content:
            l = line.split()
            if len(l) < 4:
                interface = line[:15].strip(),
                status = line[15:40].strip()
                protocol = line[40:].strip()
                description = ""
            else:
                interface = l[0].strip()
                status = l[1].strip()
                protocol = l[2].strip()
                description = " ".join(l[3:]).strip()
            res[interface] = (description, status, protocol, line)
        return res

class NexusDesParser(InterfaceDescriptionParser):
    def __init__(self):
        self.cmd = 'show interface status'

    def parse(self, raw):
        if not raw:
            return {}
        res = {}
        content = [l for l in raw.split('\n')[4:] if l.strip() != ""]

        for line in content:
            interface = line[:14].strip()
            status = line[32:42].strip()
            protocol = line[42:50].strip()
            description = line[14:32].strip()
            res[interface] = (description, status, protocol, line)
        return res

class IGMPGroupParser():
    def parse(self, raw):
        pass
    
    def parse_from_shell(self, ssh):
        return self.parse(ssh.send_command(self.cmd))


class AristaIGMPGroupParser(IGMPGroupParser):
    def __init__(self):
        self.cmd = "show ip igmp snooping group"

    def parse(self, raw):
        if not raw:
            return {}
        res = {}
        raw_content = [l for l in raw.split('\n')[2:] if l.strip() != ""]
        content = []
        for i in range(len(raw_content)):
            if raw_content[i][:50].strip() == "" and raw_content[i-1].strip()[-1] == ',':
                content[-1] += raw_content[i].strip()
            else:
                content.append(raw_content[i].strip()) 

        for line in content:
            group = line[6:22].strip()
            if len(group.split('.')) == 4:
                ports = [p.strip() for p in line[50:].strip().split(',') if p.strip() != "" and p.strip() != 'Cpu']
                for pt in ports:
                    res.setdefault(group, []).append(pt)
        return res

class CatalystIGMPGroupParser(IGMPGroupParser):
    def __init__(self):
        self.cmd = "show ip igmp snooping group"
    
    def parse(self, raw):
        if not raw:
            return {}
        res = {}
        raw_content = [l for l in raw.split('\n')[2:] if l.strip() != ""]
        content = []
        for i in range(len(raw_content)):
            if raw_content[i][:50].strip() == "" and raw_content[i-1].strip()[-1] == ',':
                content[-1] += raw_content[i].strip()
            else:
                content.append(raw_content[i].strip())
        
        for line in content:
            group = line[10:25]
            if len(group.split('.')) == 4:
                l = re.split(r'v2|v3', line)
                if len(l) != 2:
                    l = re.split(r'igmp', line)
                for pt in l[-1].split(','):
                    res.setdefault(group, []).append(pt.strip())
        return res

class NexusIGMPGroupParser(IGMPGroupParser):
    def __init__(self):
        self.cmd = "show ip igmp snooping group"

    def parse(self, raw):
        if not raw:
            return {}
        res = {}
        content = [l for l in raw.split('\n')[3:] if l.strip() != ""]
        for l in content:
            group = l[6:21].strip()
            if len(group.split('.')) == 4:
                for pt in l[36:].split():
                    res.setdefault(group, []).append(pt.strip())
      

        return res

class Main:
    def __init__(self, sw):
        self.ssh = SSHClient(sw)
        self.des_parser = self._get_int_des_parser(sw)
        self.group_parser = self._get_igmp_group_parser(sw)

    def _get_int_des_parser(self, sw):
        d = {
            'arista': AristaIntDesParser(),
            'catalyst': CatalystDesParser(),
            'nexus': NexusDesParser()
        }
        return d.get(sw.model)
    
    def _get_igmp_group_parser(self, sw):
        d = {
            'arista': AristaIGMPGroupParser(),
            'catalyst': CatalystIGMPGroupParser(),
            'nexus': NexusIGMPGroupParser()
        }
        return d.get(sw.model)

    def run(self):
        int_descriptions = self.des_parser.parse_from_shell(self.ssh)
        igmp_groups = self.group_parser.parse_from_shell(self.ssh)

        for k, v in igmp_groups.items():
            group, created = IGMPSnoopingGroup.objects.get_or_create(
                multicastGroup = k
            )

            if created:
                self.add_feed_relationship(group)

            #print('IGMP Group', k)
            for prt in v:
                desc = int_descriptions.get(prt)
                # desc => (description, status, protocol, line)
                if desc and 'down' not in desc[1].lower() and 'down' not in desc[2]:
                    update_val = {
                        "description" : desc[0],
                        "status" : desc[1],
                        "protocol" : desc[2],
                        "line" : desc[3]
                    }
                    intDescr, created = InterfaceDescription.objects.update_or_create(
                        switchIP = self.ssh.swip,
                        interface = prt,
                        defaults = update_val
                    )
                    
                    if created:
                        self.handle_new_description(intDescr, group)
             
                    #creating monthly access records 
                    try:
                        record, a_created = AccessRecord.objects.get_or_create(
                                              interface=intDescr,
                                              multicastGroup=group,
                                              year="%4d" %dt.today().year,
                                              month="%02d" %dt.today().month)
                        if a_created: 
                            print('new access record created')
                    except:
                        traceback.print_exc()

                    # creating daily access records
                    try:
                        record, a_created = DailyAccessRecord.objects.get_or_create(
                                              interface=intDescr,
                                              multicastGroup=group,
                                              year="%4d" %dt.today().year,
                                              month="%02d" %dt.today().month,
                                              day="%02d" %dt.today().day)
                        if a_created: 
                            print('new daily access record created')
                    except:
                        traceback.print_exc()
                else:
                    print(desc)

    
    def add_feed_relationship(self, group):
        for feed in Feed.objects.all().filter(
            multicastGroup=group.multicastGroup):
            print("LINKING FEED-GROUP:", feed)
            feed.group = group
            feed.save()
    
    def handle_new_description(self, intDescr, group):
        group.interfaces.add(intDescr)
        group.save()
        if intDescr.description.strip() != "":
            self.handle_server_owner(intDescr)


    def handle_server_owner(self, intDescr):
        server_name = intDescr.description.split()[0].strip()
        server, created = Server.objects.get_or_create(hostname=server_name)
        intDescr.server = server
        intDescr.save()

        customer_tag = server.hostname.split('-')[0].strip().upper()
        try:
            customer = Customer.objects.get(tag=customer_tag)
        except:
            print("CUTOMER NOT FOUND:", customer_tag)
            customer = None
        if customer:
            server.owner = customer
            server.save()


        

def test_arista():
    for sw in Switch.objects.all().filter(model="arista"):
        ssh = SSHClient(sw)
        #res = ssh.send_command('show interface description')
        res = ssh.send_command('show ip igmp snooping group')
        #parser = AristaIntDesParser()
        parser = AristaIGMPGroupParser()
        for k,v in parser.parse(res).items():
            print(k,v)


def test_catalyst():
    for sw in Switch.objects.all().filter(model="catalyst"):
        ssh = SSHClient(sw)
        #res = ssh.send_command('show interface description')
        res = ssh.send_command('show ip igmp snooping group')
        #parser = CatalystDesParser()
        parser = CatalystIGMPGroupParser()
        for k,v in parser.parse(res).items():
            print(k,v)


def test_nexus():
    for sw in Switch.objects.all().filter(model="nexus"):
        ssh = SSHClient(sw)
        #res = ssh.send_command('show interface status')
        res = ssh.send_command('show ip igmp snooping group')
        #parser = NexusDesParser()
        parser = NexusIGMPGroupParser()
        for k,v in parser.parse(res).items():
            print(k,v)



if __name__ == '__main__':
    
    for sw in Switch.objects.all():
        app = Main(sw)
        app.run()
    
    #test_arista()
    #test_catalyst()
    #test_nexus()
   
