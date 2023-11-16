# Generated by Django 4.2.6 on 2023-11-16 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('technical', '0071_rename_lpo_no_inhousetickets_telephone_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='InhouseTSignature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signature_image', models.ImageField(upload_to='signatures/')),
                ('approved', models.CharField(max_length=255)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='technical.inhousetickets')),
            ],
        ),
    ]
