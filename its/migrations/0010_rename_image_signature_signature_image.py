# Generated by Django 4.2.6 on 2023-10-18 13:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('its', '0009_alter_signature_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='signature',
            old_name='image',
            new_name='signature_image',
        ),
    ]
