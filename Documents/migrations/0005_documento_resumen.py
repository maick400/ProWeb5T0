# Generated by Django 4.1.6 on 2023-02-23 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Documents', '0004_tipodocumento_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='documento',
            name='resumen',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
