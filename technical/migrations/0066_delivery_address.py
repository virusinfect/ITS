# Generated by Django 4.2.6 on 2023-11-09 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('technical', '0065_alter_items_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='address',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
