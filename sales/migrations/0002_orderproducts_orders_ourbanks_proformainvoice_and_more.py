# Generated by Django 4.2.6 on 2023-10-23 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderProducts',
            fields=[
                ('op_id', models.AutoField(primary_key=True, serialize=False)),
                ('product', models.TextField()),
                ('quantity', models.IntegerField()),
                ('date_ordered', models.DateTimeField()),
                ('supplier', models.TextField()),
                ('date_received', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'order_products',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('o_id', models.AutoField(primary_key=True, serialize=False)),
                ('client', models.TextField()),
                ('lpo_no', models.TextField()),
                ('status', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'orders',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='OurBanks',
            fields=[
                ('bank_id', models.AutoField(primary_key=True, serialize=False)),
                ('bank', models.TextField()),
                ('ac_name', models.TextField()),
                ('address', models.TextField()),
                ('branch', models.TextField()),
                ('ac_no', models.TextField()),
                ('bank_code', models.TextField()),
                ('branch_code', models.TextField()),
                ('swift_code', models.TextField()),
                ('currency', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'our_banks',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProformaInvoice',
            fields=[
                ('pfq_id', models.AutoField(primary_key=True, serialize=False)),
                ('ref_no', models.CharField(max_length=255)),
                ('mail_text', models.CharField(max_length=1000)),
                ('footer_note', models.CharField(max_length=1000)),
                ('currency', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=255)),
                ('vat_stats', models.TextField()),
                ('remark', models.TextField()),
                ('notes', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('sent_stats', models.IntegerField()),
            ],
            options={
                'db_table': 'proforma_invoice',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SalesQuoteProducts',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('part_no', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=2000)),
                ('price', models.FloatField()),
                ('quantity', models.FloatField()),
                ('attachment', models.CharField(max_length=1000)),
                ('currency', models.CharField(max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('availability', models.TextField()),
            ],
            options={
                'db_table': 'sales_quote_products',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SalesQuotes',
            fields=[
                ('sq_id', models.AutoField(primary_key=True, serialize=False)),
                ('ref_no', models.CharField(max_length=255)),
                ('mail_text', models.TextField(max_length=2500)),
                ('footer_note', models.TextField(max_length=3000)),
                ('currency', models.CharField(max_length=3)),
                ('status', models.CharField(max_length=255)),
                ('layout', models.CharField(max_length=255)),
                ('vat_stats', models.CharField(max_length=255)),
                ('remark', models.TextField()),
                ('notes', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('sent_stats', models.IntegerField()),
            ],
            options={
                'db_table': 'sales_quotes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SalesTicketProducts',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('part_no', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.FloatField()),
                ('quantity', models.FloatField()),
                ('currency', models.TextField()),
                ('availability', models.CharField(max_length=255)),
                ('supplier', models.CharField(max_length=255)),
                ('attachment', models.CharField(max_length=5000)),
                ('is_active', models.IntegerField(default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'sales_ticket_products',
                'managed': False,
            },
        ),
    ]
