# Generated by Django 4.2.6 on 2023-10-25 08:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('its', '0011_delete_signature'),
        ('technical', '0032_tsourcing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serviceschedules',
            name='company_id',
        ),
        migrations.AddField(
            model_name='serviceschedules',
            name='company',
            field=models.ForeignKey(db_column='company_id', default=1, on_delete=django.db.models.deletion.CASCADE, to='its.company'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tsourcing',
            name='availability',
            field=models.CharField(max_length=255),
        ),
    ]
