# Generated by Django 4.2.6 on 2023-10-14 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('technical', '0011_alter_delivery_department_alter_delivery_remarks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='signature',
            field=models.ImageField(null=True, upload_to='signatures/'),
        ),
    ]
