# Generated by Django 4.2.6 on 2023-11-07 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('technical', '0057_technicalreport'),
    ]

    operations = [
        migrations.AddField(
            model_name='technicalreport',
            name='sent_approval',
            field=models.BooleanField(default=False),
        ),
    ]