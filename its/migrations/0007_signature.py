# Generated by Django 4.2.6 on 2023-10-18 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('its', '0006_task_creator'),
    ]

    operations = [
        migrations.CreateModel(
            name='Signature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='signatures/')),
            ],
        ),
    ]
