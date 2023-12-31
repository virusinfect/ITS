# Generated by Django 4.2.6 on 2023-10-30 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('its', '0012_task_updated'),
        ('technical', '0044_service_checklistitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='its.clients')),
            ],
        ),
        migrations.RemoveField(
            model_name='report',
            name='machine',
        ),
        migrations.RemoveField(
            model_name='checklist',
            name='data',
        ),
        migrations.RemoveField(
            model_name='checklist',
            name='machine_type',
        ),
        migrations.RemoveField(
            model_name='checklistitem',
            name='Machine',
        ),
        migrations.AddField(
            model_name='checklistitem',
            name='checklist',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='technical.checklist'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Machine',
        ),
        migrations.DeleteModel(
            name='MachineType',
        ),
        migrations.DeleteModel(
            name='Report',
        ),
        migrations.AddField(
            model_name='checklist',
            name='equipment',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='technical.equipment'),
            preserve_default=False,
        ),
    ]
