# Generated by Django 4.1.6 on 2023-02-14 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Documents', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documento',
            name='ruta',
            field=models.FileField(blank=True, null=True, upload_to='documents'),
        ),
    ]
