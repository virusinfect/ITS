# Generated by Django 4.2.6 on 2023-11-23 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prices', '0010_fellowespricelist'),
    ]

    operations = [
        migrations.AddField(
            model_name='coloursoftpricelist',
            name='hp_code',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='coloursoftpricelist',
            name='brand',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
