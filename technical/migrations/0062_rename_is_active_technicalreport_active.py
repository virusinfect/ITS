# Generated by Django 4.2.6 on 2023-11-07 12:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('technical', '0061_technicalreport_is_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='technicalreport',
            old_name='is_active',
            new_name='active',
        ),
    ]