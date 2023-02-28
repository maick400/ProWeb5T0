# Generated by Django 4.1.6 on 2023-02-10 05:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tipodocumento',
            fields=[
                ('idtipodocumento', models.BigAutoField(primary_key=True, serialize=False)),
                ('tipo', models.CharField(blank=True, max_length=30, null=True, unique=True)),
                ('descripcion', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'tipodocumento',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('iddocumento', models.BigAutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(blank=True, max_length=100, null=True)),
                ('fechasubida', models.DateTimeField(auto_now_add=True)),
                ('ruta', models.FileField(blank=True, null=True, upload_to='documents/%Y/%m/%d')),
                ('estado', models.CharField(blank=True, max_length=20, null=True)),
                ('idtipodocumento', models.ForeignKey(blank=True, db_column='idtipodocumento', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Documents.tipodocumento')),
            ],
            options={
                'db_table': 'documento',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Detalledocumento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('atributo', models.CharField(blank=True, max_length=100, null=True)),
                ('tipodato', models.CharField(blank=True, max_length=100, null=True)),
                ('valor', models.CharField(blank=True, max_length=100, null=True)),
                ('iddocumento', models.ForeignKey(blank=True, db_column='iddocumento', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Documents.documento')),
            ],
            options={
                'db_table': 'detalledocumento',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Basedocumento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('atributo', models.CharField(blank=True, max_length=100, null=True)),
                ('tipodato', models.CharField(blank=True, max_length=100, null=True)),
                ('idtipodocumento', models.ForeignKey(blank=True, db_column='idtipodocumento', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Documents.tipodocumento')),
            ],
            options={
                'db_table': 'basedocumento',
                'managed': True,
            },
        ),
    ]
