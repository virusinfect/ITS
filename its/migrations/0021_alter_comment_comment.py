# Generated by Django 4.2.6 on 2024-01-08 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('its', '0020_task_completed_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.CharField(max_length=255),
        ),
    ]