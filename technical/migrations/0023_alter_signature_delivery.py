# Generated by Django 4.2.6 on 2023-10-19 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('technical', '0022_remove_delivery_signature_signature'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signature',
            name='delivery',
            field=models.IntegerField(null=True),
        ),
    ]
