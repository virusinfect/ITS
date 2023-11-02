# Generated by Django 4.2.6 on 2023-10-24 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('technical', '0028_signature_delivery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='delivery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='technical.delivery'),
        ),
    ]
