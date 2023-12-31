# Generated by Django 4.2.6 on 2023-10-25 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('technical', '0033_remove_serviceschedules_company_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='amount',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='vat_status',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='items',
            name='quantity',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='serviceschedules',
            name='status',
            field=models.CharField(default='Awaiting confirmation', max_length=255),
        ),
    ]
