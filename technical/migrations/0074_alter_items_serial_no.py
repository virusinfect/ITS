# Generated by Django 4.2.6 on 2023-11-22 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('technical', '0073_alter_inhousetickets_tr_approval_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='serial_no',
            field=models.TextField(null=True),
        ),
    ]
