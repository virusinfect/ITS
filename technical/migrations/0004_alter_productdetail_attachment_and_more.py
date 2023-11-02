# Generated by Django 4.2.6 on 2023-10-13 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('technical', '0003_alter_productdetail_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productdetail',
            name='attachment',
            field=models.FileField(null=True, upload_to='attachments/'),
        ),
        migrations.AlterField(
            model_name='productdetail',
            name='availability',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='productdetail',
            name='currency',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='productdetail',
            name='price',
            field=models.DecimalField(decimal_places=2, default=100, max_digits=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='productdetail',
            name='supplier',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
