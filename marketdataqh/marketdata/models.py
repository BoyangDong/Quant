from django.db import models

# Create your models here.
class Feed(models.Model):
    #id = models.AutoField(primary_key=True)
    multicastGroup = models.CharField(max_length=15)
    port = models.IntegerField(blank=True, null=True)
    protocol = models.CharField(max_length=64, blank=True, null=True)
    feedName = models.CharField(max_length=64, blank=True, null=True)
    feedType = models.CharField(max_length=64, blank=True, null=True)
    sessionName = models.CharField(max_length=256, blank=True, null=True)
    connectionType = models.CharField(max_length=64, blank=True, null=True)
    channel = models.CharField(max_length=64, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    lastEdited = models.DateTimeField(auto_now=True, null=True)
    group = models.ForeignKey('IGMPSnoopingGroup', on_delete=models.SET_NULL, null=True)

    def __repr__(self):
        return "%s\t%s\t%s\t%d" %(self.feedName, self.feedType, self.multicastGroup, self.port)
    
    def __str__(self):
        return self.__repr__()

#print("\t".join([feed_name, feed_type, ip_address, str(port), protocol, connection_type, channel]))


class Switch(models.Model):
    #id = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=15, unique=True)
    model = models.CharField(max_length=64)
    isActive = models.BooleanField(default=True)


    def __repr__(self):
        return "%15s\t%s" %(self.ip, self.model)
    
    def __str__(self):
        return self.__repr__()

class Customer(models.Model):
    #id = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=64)
    isActive = models.BooleanField(default=True)

    def __repr__(self):
        return "<%s> %s" %(self.tag, self.name)
        
    def __str__(self):
        return self.__repr__()


class Server(models.Model):
    #id = models.AutoField(primary_key=True)
    hostname = models.CharField(max_length=64, unique=True)
    owner = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return "%s\t%s" %(self.hostname, self.owner or "")
    def __repr__(self):
        return self.__str__()

class InterfaceDescription(models.Model):
    #id = models.AutoField(primary_key=True)
    switchIP = models.CharField(max_length=15, null=False)
    interface = models.CharField(max_length=16, null=False, blank=True)
    description = models.CharField(max_length=64)
    status = models.CharField(max_length=64, blank=True)
    protocol = models.CharField(max_length=64, blank=True)
    line = models.CharField(max_length=256)
    server = models.ForeignKey('Server', on_delete=models.SET_NULL, null=True)

    def __repr__(self):
        return "%s %s" %(self.description, self.server)
    
    def __str__(self):
        return self.__repr__()

    class Meta:
        unique_together = (("switchIP", "interface"))


class IGMPSnoopingGroup(models.Model):
    #id = models.AutoField(primary_key=True)
    interfaces = models.ManyToManyField('InterfaceDescription')
    multicastGroup = models.CharField(max_length=15, unique=True)

    def __repr__(self):
        return self.multicastGroup

    def __str__(self):
        return self.__repr__()
    


class AccessRecord(models.Model):
    #id = models.AutoField(primary_key=True)
    interface = models.ForeignKey('InterfaceDescription', on_delete=models.CASCADE)
    multicastGroup = models.ForeignKey('IGMPSnoopingGroup', on_delete=models.CASCADE)
    year = models.CharField(max_length=4)
    month = models.CharField(max_length=2)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = (("interface", "multicastGroup", "year", "month"))



class DailyAccessRecord(models.Model):
    #id = models.AutoField(primary_key=True)
    interface = models.ForeignKey('InterfaceDescription', on_delete=models.CASCADE)
    multicastGroup = models.ForeignKey('IGMPSnoopingGroup', on_delete=models.CASCADE)
    year = models.CharField(max_length=4)
    month = models.CharField(max_length=2)
    day = models.CharField(max_length=2)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = (("interface", "multicastGroup", "year", "month", "day"))
    