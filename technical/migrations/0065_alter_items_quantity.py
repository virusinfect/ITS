# Generated by Django 4.2.6 on 2023-11-09 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('technical', '0064_ticketimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='quantity',
            field=models.IntegerField(null=True),
        ),
    ]
