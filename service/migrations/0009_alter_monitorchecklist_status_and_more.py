# Generated by Django 4.2.6 on 2023-11-02 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0008_remove_service_observations_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitorchecklist',
            name='status',
            field=models.TextField(default='Pending'),
        ),
        migrations.AlterField(
            model_name='printerchecklist',
            name='status',
            field=models.TextField(default='Pending'),
        ),
        migrations.AlterField(
            model_name='upschecklist',
            name='status',
            field=models.TextField(default='Pending'),
        ),
    ]