# Generated by Django 4.2.6 on 2023-10-18 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('its', '0007_signature'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signature',
            name='image',
            field=models.BinaryField(),
        ),
    ]
