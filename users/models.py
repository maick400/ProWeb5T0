from django.db import models

# Create your models here.
class Rol(models.Model):
    idrol = models.IntegerField(primary_key=True)
    nombrerol = models.CharField(max_length=15, blank=True, null=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rol'


class Usuario(models.Model):
    idusuario = models.IntegerField(primary_key=True)
    idrol = models.ForeignKey(Rol, models.DO_NOTHING, db_column='idrol')
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    correo = models.CharField(unique=True, max_length=50)
    fechanacimiento = models.TimeField()
    contrasenia = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'usuario'


