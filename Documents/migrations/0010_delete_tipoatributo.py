# Generated by Django 4.1.6 on 2023-02-26 23:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Documents', '0009_alter_basedocumento_tipodato_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TipoAtributo',
        ),
    ]