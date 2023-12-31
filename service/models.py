from django.db import models
from technical.models import ServiceTickets
from its.models import Company, Clients
from django.contrib.auth.models import User

class Service(models.Model):
    ticket = models.ForeignKey(ServiceTickets, on_delete=models.CASCADE)
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    details = models.TextField()
    status = models.TextField()
    created = models.DateTimeField(auto_now_add=True)  # Automatically set upon creation
    updated = models.DateTimeField(auto_now=True)  # Automatically updated on each save

    def __str__(self):
        return f"{self.ticket} - {self.client}"


class Equipment(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    serial_no = models.CharField(max_length=100)
    details = models.TextField()
    type = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)  # Automatically set upon creation
    updated = models.DateTimeField(auto_now=True)  # Automatically updated on each save

    def __str__(self):
        return f"{self.name} - {self.client}"

class ServiceQuote(models.Model):
    part_no = models.CharField(max_length=255)
    description = models.CharField(max_length=2000)
    price = models.FloatField()
    quantity = models.FloatField()
    attachment = models.CharField(max_length=1000, null=True)
    currency = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    ticket = models.ForeignKey(ServiceTickets, on_delete=models.CASCADE)
    availability = models.CharField(max_length=255, null=True)

class Software(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    os = models.CharField(max_length=100, null=True)
    mo = models.CharField(max_length=100, null=True)
    backup = models.CharField(max_length=100, null=True)
    outlook = models.CharField(max_length=100, null=True)
    created = models.DateTimeField(auto_now_add=True)  # Automatically set upon creation
    updated = models.DateTimeField(auto_now=True)  # Automatically updated on each save

    def __str__(self):
        return f"Software for {self.client}"


class EquipmentSpecs(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    antivirus = models.CharField(max_length=100)
    psu = models.CharField(max_length=100)
    domain = models.CharField(max_length=100,blank=True)
    comp_name = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=100)
    ram = models.CharField(max_length=100)
    cd_dvd = models.CharField(max_length=100)
    processor = models.CharField(max_length=100)
    gen = models.CharField(max_length=100,null=True)
    hdd = models.CharField(max_length=100)
    hdd_status = models.CharField(max_length=100)
    mainboard = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)  # Automatically set upon creation
    updated = models.DateTimeField(auto_now=True)  # Automatically updated on each save

    def __str__(self):
        return f"Specs for {self.equipment}"


class MonitorChecklist(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    phy_damage = models.BooleanField(null=True)
    colour_display = models.BooleanField(null=True)
    vertical_lines = models.BooleanField(null=True)
    vga_cable = models.BooleanField(null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    status = models.TextField(default="Pending")
    observations = models.TextField()
    recommendation = models.TextField()



class PrinterChecklist(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    power = models.BooleanField(null=True)
    tone = models.BooleanField(null=True)
    phy_damage = models.BooleanField(null=True)
    service_interior = models.BooleanField(null=True)
    service_roller = models.BooleanField(null=True)
    static_eliminator = models.BooleanField(null=True)
    fuser_unit = models.BooleanField(null=True)
    gears = models.BooleanField(null=True)
    status = models.TextField(default="Pending")
    observations = models.TextField()
    recommendation = models.TextField()


class UpsChecklist(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    power = models.BooleanField(null=True)
    backup = models.BooleanField(null=True)
    ports = models.BooleanField(null=True)
    battery = models.BooleanField(null=True)
    phy_damage = models.BooleanField(null=True)
    status = models.TextField(default="Pending")
    observations = models.TextField()
    recommendation = models.TextField()


class CpuChecklist(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    antiv = models.BooleanField(null=True)
    pwr = models.BooleanField(null=True)
    memory = models.BooleanField(null=True)
    fan = models.BooleanField(null=True)
    dvd = models.BooleanField(null=True)
    processor = models.BooleanField(null=True)
    hdd = models.BooleanField(null=True)
    board = models.BooleanField(null=True)
    status = models.TextField(default="Pending")
    observations = models.TextField()
    recommendation = models.TextField()

class ServerChecklist(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    antiv = models.BooleanField(null=True)
    pwr = models.BooleanField(null=True)
    memory = models.BooleanField(null=True)
    fan = models.BooleanField(null=True)
    dvd = models.BooleanField(null=True)
    processor = models.BooleanField(null=True)
    hdd = models.BooleanField(null=True)
    board = models.BooleanField(null=True)
    status = models.TextField(default="Pending")
    observations = models.TextField()
    recommendation = models.TextField()

class LaptopChecklist(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    antiv = models.BooleanField(null=True)
    pwr = models.BooleanField(null=True)
    memory = models.BooleanField(null=True)
    fan = models.BooleanField(null=True)
    dvd = models.BooleanField(null=True)
    processor = models.BooleanField(null=True)
    hdd = models.BooleanField(null=True)
    board = models.BooleanField(null=True)
    status = models.TextField(default="Pending")
    observations = models.TextField()
    recommendation = models.TextField()