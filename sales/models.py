from django.contrib.auth.models import User
from django.db import models
from its.models import Company,Task


class SalesTickets(models.Model):
    ticket_id = models.AutoField(primary_key=True)  # Change to AutoField
    status = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    issue_summary = models.TextField()
    description = models.CharField(max_length=255)
    via = models.CharField(max_length=255)
    handler = models.ForeignKey(User, on_delete=models.CASCADE, db_column='handler_id')
    more = models.CharField(max_length=500)
    is_active = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='company_id')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='created_by')

    class Meta:
        managed = False
        db_table = 'sales_tickets'


class SalesTicketProducts(models.Model):
    product_id = models.AutoField(primary_key=True)
    part_no = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField(default="0",null=True)
    quantity = models.FloatField(default="0")
    currency = models.TextField(blank=True)
    availability = models.CharField(max_length=255,blank=True)
    supplier = models.CharField(max_length=255,blank=True)
    attachment = models.ImageField(upload_to='att/', blank=True, null=True)
    is_active = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    ticket = models.ForeignKey(SalesTickets, on_delete=models.CASCADE, db_column='ticket_id')

    class Meta:
        managed = False
        db_table = 'sales_ticket_products'

class SalesQuotes(models.Model):
    sq_id = models.AutoField(primary_key=True)
    mail_text = models.TextField(max_length=2500)  # Changed to TextField
    footer_note = models.TextField(max_length=3000)  # Changed to TextField
    currency = models.CharField(max_length=3)  # Use a CharField for currency codes (e.g., USD, EUR)
    status = models.CharField(max_length=255)
    layout = models.CharField(max_length=255)
    vat_stats = models.CharField(max_length=255)  # Corrected the field name
    remark = models.TextField()
    notes = models.TextField()
    is_active = models.BooleanField(default=True)  # Changed to BooleanField
    created = models.DateTimeField(auto_now_add=True)  # Automatically set upon creation
    updated = models.DateTimeField(auto_now=True)  # Automatically updated on each save
    ticket = models.ForeignKey(SalesTickets, on_delete=models.CASCADE,
                               db_column='ticket_id')  # Assuming SalesTickets is defined
    company = models.ForeignKey(Company, on_delete=models.CASCADE,
                                db_column='company_id')  # Assuming Company is defined
    sent_stats = models.IntegerField()  # Consider using a BooleanField or choices for status
    quote_handler = models.ForeignKey(User, on_delete=models.CASCADE,
                                      db_column='quote_handler')

    class Meta:
        managed = False
        db_table = 'sales_quotes'


class SalesQuoteProducts(models.Model):
    product_id = models.AutoField(primary_key=True)
    part_no = models.CharField(max_length=255)
    description = models.CharField(max_length=2000)
    price = models.FloatField()
    quantity = models.FloatField()
    attachment = models.ImageField(upload_to='sales_images/')
    currency = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    quote = models.ForeignKey(SalesQuotes, on_delete=models.CASCADE,
                              db_column='sq_id')
    availability = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'sales_quote_products'


class Orders(models.Model):
    o_id = models.AutoField(primary_key=True)
    client = models.TextField()
    lpo_no = models.TextField()
    assignee = models.ForeignKey(User, on_delete=models.CASCADE,
                                 db_column='assignee')
    status = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    ticket = models.ForeignKey(SalesTickets, on_delete=models.CASCADE,
                               db_column='ticket_id', null=True)

    class Meta:
        managed = False
        db_table = 'orders'


class OurBanks(models.Model):
    bank_id = models.AutoField(primary_key=True)
    bank = models.TextField()
    ac_name = models.TextField()
    address = models.TextField()
    branch = models.TextField()
    ac_no = models.TextField()
    bank_code = models.TextField()
    branch_code = models.TextField()
    swift_code = models.TextField()
    currency = models.TextField()
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bank

    class Meta:
        managed = False
        db_table = 'our_banks'


class ProformaInvoice(models.Model):
    pfq_id = models.AutoField(primary_key=True)
    ref_no = models.CharField(max_length=255,null=True)
    currency = models.CharField(max_length=255,null=True)
    status = models.CharField(max_length=255)
    vat_stats = models.TextField()
    remark = models.TextField()
    layout = models.CharField(max_length=255,null=True)
    notes = models.TextField()
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    ticket = models.ForeignKey(SalesTickets, on_delete=models.CASCADE,
                               db_column='ticket_id', null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE,
                                db_column='company_id')
    sent_stats = models.IntegerField(default=0)
    invoice_handler = models.ForeignKey(User, on_delete=models.CASCADE,
                                        db_column='invoice_handler')
    bank = models.ForeignKey(OurBanks, on_delete=models.CASCADE,
                             db_column='bank',default=1)

    class Meta:
        managed = False
        db_table = 'proforma_invoice'


class OrderProducts(models.Model):
    op_id = models.AutoField(primary_key=True)
    product = models.TextField()
    quantity = models.FloatField()
    date_ordered = models.DateField(null=True, blank=True, default=None)
    supplier = models.TextField()
    date_received = models.DateField(null=True, blank=True, default=None)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    orders = models.ForeignKey(Orders, on_delete=models.CASCADE, db_column='o_id')

    class Meta:
        managed = False
        db_table = 'order_products'


class ProformaInvoiceProducts(models.Model):
    product_id = models.AutoField(primary_key=True)
    part_no = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.FloatField()
    quantity = models.FloatField()
    availability = models.CharField(max_length=255)
    currency = models.CharField(max_length=50)
    is_active = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    pfi = models.ForeignKey(ProformaInvoice, on_delete=models.CASCADE, db_column='pfq_id')

    class Meta:
        managed = False
        db_table = 'proforma_invoice_products'



