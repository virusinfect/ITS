# Generated by Django 4.2.6 on 2023-10-30 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('its', '0012_task_updated'),
        ('technical', '0047_checklist_checklistitem_equipment_service_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='client',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='its.clients'),
            preserve_default=False,
        ),
    ]
