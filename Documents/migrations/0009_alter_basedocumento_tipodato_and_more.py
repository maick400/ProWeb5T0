# Generated by Django 4.1.6 on 2023-02-26 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Documents', '0008_remove_basedocumento_idtipoatributo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basedocumento',
            name='tipodato',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='detalledocumento',
            name='atributo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='detalledocumento',
            name='tipodato',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
