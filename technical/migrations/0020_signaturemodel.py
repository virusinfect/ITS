# Generated by Django 4.2.6 on 2023-10-19 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('technical', '0019_remove_delivery_signature_image_delivery_signature'),
    ]

    operations = [
        migrations.CreateModel(
            name='SignatureModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signature', models.TextField()),
            ],
        ),
    ]
