# Generated by Django 4.2.6 on 2023-12-04 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prices', '0015_type_laptoppricelist_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='pricerule',
            name='constant',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='pricerule',
            name='discount_percentage',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='pricerule',
            name='discount_percentage2',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='type',
            name='name',
            field=models.CharField(max_length=250),
        ),
    ]
