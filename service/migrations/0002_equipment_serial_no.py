# Generated by Django 4.2.6 on 2023-11-01 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='serial_no',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
