# Generated by Django 4.2.6 on 2024-01-05 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('technical', '0076_servicetickets_aiosdone_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='csignature',
            name='approved',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
