from django.db import models

# Create your models here.

class Basedocumento(models.Model):
    idtipodocumento = models.ForeignKey('Tipodocumento', models.DO_NOTHING, db_column='idtipodocumento', blank=True, null=True)
    atributo = models.CharField(max_length=100, blank=True, null=True)
    tipodato = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'basedocumento'


class Detalledocumento(models.Model):
    iddocumento = models.ForeignKey('Documento', models.DO_NOTHING, db_column='iddocumento', blank=True, null=True)
    atributo = models.CharField(max_length=100, blank=True, null=True)
    tipodato = models.CharField(max_length=100, blank=True, null=True)
    valor = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'detalledocumento'
        
        
class Documento(models.Model):
    iddocumento = models.BigAutoField(primary_key=True)
    idtipodocumento = models.ForeignKey('Tipodocumento', models.DO_NOTHING, db_column='idtipodocumento', blank=True, null=True)
    titulo = models.CharField( max_length=100, blank=True, null=True)
    portada = models.ImageField(upload_to='documents/portadas', blank=True, null=True)
    fechasubida = models.DateTimeField(auto_now_add=True)
    ruta = models.FileField(upload_to='documents', blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
            return self.name
    
    class Meta:
        managed = True
        db_table = 'documento'
        
        
        
    


class Tipodocumento(models.Model):
    idtipodocumento = models.BigAutoField(primary_key=True)
    imagen = models.ImageField(upload_to= 'documents/category_type', blank=True, null=True)
    tipo = models.CharField(unique=True, max_length=30, blank=True, null=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tipodocumento'
    # def __str__(self):
    #     return self.tipo
