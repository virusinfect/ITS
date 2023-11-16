import uuid
from datetime import time, timezone,datetime

from django.contrib.auth.models import User
from django.db import models
from its.models import Company, Clients, Parts, Task


class Tickets(models.Model):
    ticket_id = models.AutoField(primary_key=True, db_comment='PK')
    priority = models.CharField(max_length=255, default=1)
    status = models.CharField(max_length=255, default="Open")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='company_id')
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, db_column='client_id')
    tech = models.ForeignKey(User, on_delete=models.CASCADE, db_column='tech_id', related_name='tickets_tech')
    equipment = models.CharField(max_length=255, null=True)
    serial_no = models.CharField(max_length=255, null=True)
    eqpass = models.CharField(max_length=255, blank=True,null=True)
    machine_yom = models.CharField(max_length=255, blank=True)
    ram = models.CharField(max_length=255, blank=True)
    rom = models.CharField(max_length=255, blank=True)
    processor = models.CharField(max_length=255, blank=True)
    os = models.CharField(max_length=255, blank=True)
    office_suite = models.CharField(max_length=255, blank=True)
    printer_yom = models.CharField(max_length=255, blank=True)
    printer_type = models.CharField(max_length=255, blank=True)
    catridge = models.CharField(max_length=255, blank=True)
    fault = models.CharField(max_length=255, blank=True)
    accessories = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    diagnosis = models.TextField(blank=True)
    action = models.TextField(blank=True)
    recommendation = models.TextField(blank=True)
    labour = models.FloatField(default=0)
    currency = models.CharField(max_length=50, default="KSH")
    remark = models.CharField(max_length=50, blank=True)
    lpo_no = models.CharField(max_length=255, blank=True)
    bench_status = models.CharField(max_length=25, default="Pending")
    more = models.CharField(max_length=300, blank=True)
    type = models.CharField(max_length=25)
    brought_by = models.CharField(max_length=255, blank=True)
    reg_sign = models.CharField(max_length=255, blank=True)
    collected_by = models.CharField(max_length=255, blank=True)
    dlvr_sign = models.CharField(max_length=255, blank=True)
    tr_approval = models.CharField(max_length=255, blank=True)
    is_active = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    agtsc = models.CharField(max_length=255, blank=True)
    timeline = models.CharField(max_length=255, blank=True)
    device_diagnosis = models.CharField(max_length=255, blank=True)
    sourcing_parts = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    device_repair = models.CharField(max_length=255, blank=True)
    product_currency = models.CharField(max_length=255, blank=True)
    device = models.TextField()
    tr_status = models.TextField()
    sourcing_status = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'tickets'


class InhouseTickets(models.Model):
    ticket_id = models.AutoField(primary_key=True, db_comment='PK')
    priority = models.CharField(max_length=255, default=1)
    status = models.CharField(max_length=255, default="Open")
    company = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    tech = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tech')
    equipment = models.CharField(max_length=255, null=True)
    serial_no = models.CharField(max_length=255, null=True)
    eqpass = models.CharField(max_length=255, blank=True,null=True)
    machine_yom = models.CharField(max_length=255, blank=True)
    ram = models.CharField(max_length=255, blank=True)
    rom = models.CharField(max_length=255, blank=True)
    processor = models.CharField(max_length=255, blank=True)
    os = models.CharField(max_length=255, blank=True)
    office_suite = models.CharField(max_length=255, blank=True)
    printer_yom = models.CharField(max_length=255, blank=True)
    printer_type = models.CharField(max_length=255, blank=True)
    catridge = models.CharField(max_length=255, blank=True)
    fault = models.CharField(max_length=255, blank=True)
    accessories = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    diagnosis = models.TextField(blank=True)
    action = models.TextField(blank=True)
    recommendation = models.TextField(blank=True)
    labour = models.FloatField(default=0)
    currency = models.CharField(max_length=50, default="KSH")
    remark = models.CharField(max_length=50, blank=True)
    telephone = models.CharField(max_length=255, blank=True)
    bench_status = models.CharField(max_length=25, default="Pending")
    more = models.CharField(max_length=300, blank=True)
    type = models.CharField(max_length=25)
    brought_by = models.CharField(max_length=255, blank=True)
    reg_sign = models.CharField(max_length=255, blank=True)
    collected_by = models.CharField(max_length=255, blank=True)
    dlvr_sign = models.CharField(max_length=255, blank=True)
    tr_approval = models.CharField(max_length=255, blank=True)
    is_active = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    agtsc = models.CharField(max_length=255, blank=True)
    timeline = models.CharField(max_length=255, blank=True)
    device_diagnosis = models.CharField(max_length=255, blank=True)
    sourcing_parts = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='handler')
    device_repair = models.CharField(max_length=255, blank=True)
    product_currency = models.CharField(max_length=255, blank=True)
    device = models.TextField()
    tr_status = models.TextField()
    sourcing_status = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)



class ProductDetail(models.Model):
    ticket = models.ForeignKey(Tickets, on_delete=models.CASCADE)
    part_number = models.CharField(max_length=100)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(null=True)
    currency = models.CharField(max_length=10, null=True)
    availability = models.CharField(max_length=100, null=True)
    supplier = models.CharField(max_length=100, null=True)
    attachment = models.FileField(upload_to='attachments/', null=True)

class InhouseProductDetail(models.Model):
    ticket = models.ForeignKey(InhouseTickets, on_delete=models.CASCADE)
    part_number = models.CharField(max_length=100)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(null=True)
    currency = models.CharField(max_length=10, null=True)
    availability = models.CharField(max_length=100, null=True)
    supplier = models.CharField(max_length=100, null=True)
    attachment = models.FileField(upload_to='attachments/', null=True)

class TicketImage(models.Model):
    ticket = models.ForeignKey('Tickets', on_delete=models.CASCADE)  # Replace 'YourTicketModel' with your actual ticket model
    tag = models.CharField(max_length=255)  # A varchar field for tagging the image
    image = models.ImageField(upload_to='ticket_images/')  # A field for uploading the image

    def __str__(self):
        return self.tag

class InhouseTicketImage(models.Model):
    ticket = models.ForeignKey('InhouseTickets', on_delete=models.CASCADE)  # Replace 'YourTicketModel' with your actual ticket model
    tag = models.CharField(max_length=255)  # A varchar field for tagging the image
    image = models.ImageField(upload_to='ticket_images/')  # A field for uploading the image

    def __str__(self):
        return self.tag

class Delivery(models.Model):
    ticket = models.ForeignKey(Tickets, on_delete=models.CASCADE, null=True)
    client = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    lpo = models.CharField(max_length=20, null=True)
    collected_by = models.CharField(max_length=100)
    currency = models.CharField(max_length=10, null=True)
    vat_status = models.CharField(max_length=10, null=True)
    status = models.CharField(max_length=20, null=True)
    remarks = models.TextField(null=True)
    department = models.CharField(max_length=50, null=True)
    created = models.DateTimeField(auto_now_add=True)  # Automatically set upon creation
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)  # Automatically updated on each save
    is_active = models.IntegerField(default=1)


class Items(models.Model):
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name='items')
    quantity = models.IntegerField(default=1)
    amount = models.IntegerField(default=0)
    serial_no = models.CharField(max_length=30, null=True)
    particulars = models.TextField()

    def __str__(self):
        return f"Item - Serial No: {self.serial_no}"


class Requisition(models.Model):
    req_id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(Tickets, on_delete=models.CASCADE)
    part = models.ForeignKey(Parts, on_delete=models.CASCADE)
    serial_no = models.CharField(max_length=200, null=True)
    collected_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='collected_by',
                                     related_name='collected_requisitions')
    remarks = models.CharField(max_length=200)
    req_status = models.CharField(max_length=255, default="Pending")
    issue_status = models.CharField(max_length=255)
    is_active = models.BooleanField(default=1)
    created = models.DateTimeField(auto_now_add=True)  # Automatically set upon creation
    updated = models.DateTimeField(auto_now=True)  # Automatically updated on each save
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='approved_by',
                                    related_name='approved_requisitions', null=True)
    return_status = models.CharField(max_length=255, null=True)
    return_approved_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='return_approved_by',
                                           related_name='return_approved_requisitions', null=True)
    quantity = models.IntegerField()
    price = models.FloatField(null=True)

    class Meta:
        managed = False
        db_table = 'requisitions'


class CallCards(models.Model):
    cc_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='company_id')
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, db_column='client_id')
    tech_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='tech_id',
                                related_name='technician')
    equipment = models.CharField(max_length=255)
    fault = models.CharField(max_length=255)
    remarks = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=255, default="Pending")
    type = models.CharField(max_length=255)
    is_active = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)  # Automatically set upon creation
    updated = models.DateTimeField(auto_now=True)  # Automatically updated on each save
    sign = models.ImageField(upload_to='signatures/')
    time_in = models.TimeField(default=time(0, 0))
    time_out = models.TimeField(default=time(0, 0))

    class Meta:
        managed = False
        db_table = 'call_cards'


class ServiceSchedules(models.Model):
    ss_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='company_id')
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()
    notes = models.CharField(max_length=500)
    status = models.CharField(max_length=255, default="Awaiting confirmation")
    is_active = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)  # Automatically set upon creation
    updated = models.DateTimeField(auto_now=True)  # Automatically updated on each save
    techs = models.ManyToManyField(User, related_name='service_schedules')


class ServiceTickets(models.Model):
    ticket_id = models.ForeignKey(ServiceSchedules, on_delete=models.CASCADE, db_column='ticket_ids')
    servers = models.IntegerField(null=True)
    cpus = models.IntegerField(null=True)
    laptops = models.IntegerField(null=True)
    printers = models.IntegerField(null=True)
    scanners = models.IntegerField(null=True)
    ups = models.IntegerField(null=True)
    large_ups = models.IntegerField(null=True)
    aios = models.IntegerField(null=True)
    biometrics = models.IntegerField(null=True)
    cctvs = models.IntegerField(null=True)
    highend_machines = models.IntegerField(null=True)
    nas = models.IntegerField(null=True)
    more = models.CharField(max_length=255, null=True)
    remark = models.CharField(max_length=200, null=True)


class Signature(models.Model):
    signature_image = models.ImageField(upload_to='signatures/')
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name='signatures')


class CSignature(models.Model):
    signature_image = models.ImageField(upload_to='signatures/')
    callcard = models.ForeignKey(CallCards, on_delete=models.CASCADE, related_name='signatures')


class Deliverys(models.Model):
    ticket = models.CharField(max_length=100)
    delivery_id = models.CharField(max_length=100, unique=True)
    signature_image = models.ImageField(upload_to='signatures/')


class Tsourcing(models.Model):
    ticket = models.ForeignKey(Tickets, on_delete=models.CASCADE)
    desc = models.CharField(max_length=255)
    part_no = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    qty = models.PositiveIntegerField(default=0.0, null=True)
    currency = models.CharField(max_length=50)
    availability = models.CharField(max_length=255)
    supplier = models.CharField(max_length=255)
    assignee = models.CharField(max_length=255)
    attachment = models.CharField(max_length=1000, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.desc


class tQuote(models.Model):
    part_no = models.CharField(max_length=255)
    description = models.CharField(max_length=2000)
    price = models.FloatField()
    quantity = models.FloatField()
    attachment = models.CharField(max_length=1000, null=True)
    currency = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    ticket = models.ForeignKey(Tickets, on_delete=models.CASCADE)
    availability = models.CharField(max_length=255, null=True)


class FormatApproval(models.Model):
    ticket = models.ForeignKey(Tickets, on_delete=models.CASCADE)
    app_info = models.TextField()  # Add fields for custom data
    data_info = models.TextField()  # Add fields for custom data
    is_signed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class UniqueToken(models.Model):
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    FormatApproval = models.ForeignKey(FormatApproval, on_delete=models.CASCADE)


class FSignature(models.Model):
    signature_image = models.ImageField(upload_to='signatures/')
    approved = models.CharField(max_length=255)
    format = models.ForeignKey(FormatApproval, on_delete=models.CASCADE)

class TSignature(models.Model):
    signature_image = models.ImageField(upload_to='signatures/')
    approved = models.CharField(max_length=255)
    ticket = models.ForeignKey(Tickets, on_delete=models.CASCADE)


class InhouseTSignature(models.Model):
    signature_image = models.ImageField(upload_to='signatures/')
    approved = models.CharField(max_length=255)
    ticket = models.ForeignKey(InhouseTickets, on_delete=models.CASCADE)

class TechSignature(models.Model):
    signature_image = models.ImageField(upload_to='signatures/')
    tech = models.ForeignKey(User, on_delete=models.CASCADE)

class TechnicalReport(models.Model):
    ticket = models.ForeignKey(Tickets, on_delete=models.CASCADE)
    report_text = models.TextField(blank=True)
    is_approved = models.TextField(blank=True)
    sent_approval = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Technical Report for Ticket: {self.ticket.company}"