# Generated by Django 4.2.6 on 2023-10-19 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('technical', '0022_remove_delivery_signature_signature'),
        ('its', '0010_rename_image_signature_signature_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Signature',
        ),
    ]
