# Generated by Django 4.2.6 on 2023-10-17 13:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('technical', '0016_alter_serviceschedules_from_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceschedules',
            name='techs',
            field=models.ManyToManyField(related_name='service_schedules', to=settings.AUTH_USER_MODEL),
        ),
    ]
