# Generated by Django 4.1.6 on 2023-02-15 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Documents', '0002_alter_documento_ruta'),
    ]

    operations = [
        migrations.AddField(
            model_name='documento',
            name='portada',
            field=models.ImageField(blank=True, null=True, upload_to='documents'),
        ),
    ]