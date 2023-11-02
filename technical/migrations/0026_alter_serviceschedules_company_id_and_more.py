# Generated by Django 4.2.6 on 2023-10-20 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('technical', '0025_remove_signature_delivery_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceschedules',
            name='company_id',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='servicetickets',
            name='ticket_id',
            field=models.ForeignKey(db_column='ticket_ids', on_delete=django.db.models.deletion.CASCADE, to='technical.serviceschedules'),
        ),
    ]
