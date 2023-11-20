# Generated by Django 4.2.6 on 2023-11-20 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prices', '0002_exchange'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchange',
            name='rate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
