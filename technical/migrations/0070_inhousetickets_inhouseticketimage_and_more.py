# Generated by Django 4.2.6 on 2023-11-16 09:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('its', '0019_rename_creator_task_created_by'),
        ('technical', '0069_techsignature'),
    ]

    operations = [
        migrations.CreateModel(
            name='InhouseTickets',
            fields=[
                ('ticket_id', models.AutoField(db_comment='PK', primary_key=True, serialize=False)),
                ('priority', models.CharField(default=1, max_length=255)),
                ('status', models.CharField(default='Open', max_length=255)),
                ('equipment', models.CharField(max_length=255, null=True)),
                ('serial_no', models.CharField(max_length=255, null=True)),
                ('eqpass', models.CharField(blank=True, max_length=255, null=True)),
                ('machine_yom', models.CharField(blank=True, max_length=255)),
                ('ram', models.CharField(blank=True, max_length=255)),
                ('rom', models.CharField(blank=True, max_length=255)),
                ('processor', models.CharField(blank=True, max_length=255)),
                ('os', models.CharField(blank=True, max_length=255)),
                ('office_suite', models.CharField(blank=True, max_length=255)),
                ('printer_yom', models.CharField(blank=True, max_length=255)),
                ('printer_type', models.CharField(blank=True, max_length=255)),
                ('catridge', models.CharField(blank=True, max_length=255)),
                ('fault', models.CharField(blank=True, max_length=255)),
                ('accessories', models.CharField(blank=True, max_length=255)),
                ('notes', models.TextField(blank=True)),
                ('diagnosis', models.TextField(blank=True)),
                ('action', models.TextField(blank=True)),
                ('recommendation', models.TextField(blank=True)),
                ('labour', models.FloatField(default=0)),
                ('currency', models.CharField(default='KSH', max_length=50)),
                ('remark', models.CharField(blank=True, max_length=50)),
                ('lpo_no', models.CharField(blank=True, max_length=255)),
                ('bench_status', models.CharField(default='Pending', max_length=25)),
                ('more', models.CharField(blank=True, max_length=300)),
                ('type', models.CharField(max_length=25)),
                ('brought_by', models.CharField(blank=True, max_length=255)),
                ('reg_sign', models.CharField(blank=True, max_length=255)),
                ('collected_by', models.CharField(blank=True, max_length=255)),
                ('dlvr_sign', models.CharField(blank=True, max_length=255)),
                ('tr_approval', models.CharField(blank=True, max_length=255)),
                ('is_active', models.IntegerField(default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('agtsc', models.CharField(blank=True, max_length=255)),
                ('timeline', models.CharField(blank=True, max_length=255)),
                ('device_diagnosis', models.CharField(blank=True, max_length=255)),
                ('device_repair', models.CharField(blank=True, max_length=255)),
                ('product_currency', models.CharField(blank=True, max_length=255)),
                ('device', models.TextField()),
                ('tr_status', models.TextField()),
                ('sourcing_status', models.TextField()),
                ('client', models.ForeignKey(db_column='client_id', on_delete=django.db.models.deletion.CASCADE, to='its.clients')),
                ('company', models.ForeignKey(db_column='company_id', on_delete=django.db.models.deletion.CASCADE, to='its.company')),
                ('sourcing_parts', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='handler', to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='its.task')),
                ('tech', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tech', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InhouseTicketImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='ticket_images/')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='technical.inhousetickets')),
            ],
        ),
        migrations.CreateModel(
            name='InhouseProductDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_number', models.CharField(max_length=100)),
                ('description', models.TextField(null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.PositiveIntegerField(null=True)),
                ('currency', models.CharField(max_length=10, null=True)),
                ('availability', models.CharField(max_length=100, null=True)),
                ('supplier', models.CharField(max_length=100, null=True)),
                ('attachment', models.FileField(null=True, upload_to='attachments/')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='technical.inhousetickets')),
            ],
        ),
    ]