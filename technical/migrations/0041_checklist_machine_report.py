# Generated by Django 4.2.6 on 2023-10-30 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('its', '0012_task_updated'),
        ('technical', '0040_tsourcing_attachment_tsourcing_created_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checklist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('machine_type', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('machine_type', models.CharField(max_length=100)),
                ('checklist', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='technical.checklist')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='its.company')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='its.clients')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remarks', models.TextField()),
                ('observations', models.TextField()),
                ('recommendations', models.TextField()),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='technical.machine')),
            ],
        ),
    ]
