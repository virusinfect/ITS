# Generated by Django 4.2.6 on 2023-10-14 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('technical', '0012_alter_delivery_signature'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='signature',
            field=models.ImageField(default=1, upload_to='signatures/'),
            preserve_default=False,
        ),
    ]
