from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class productos(models.Model):

    nombre = models.CharField(max_length=20)
    seccion = models.CharField(max_length=20)
    precio = models.FloatField()
    imagen = models.CharField(max_length=100)
    stock = models.IntegerField()
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)


    class Meta:
        verbose_name='producto'
        verbose_name_plural='productos'
        db_table='productos'   #nombre de la base de datos en mysql
        ordering=['id']


class perfil_datos(models.Model):
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    sexo = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    pais = models.CharField(max_length=20)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE,  default=0)

    class Meta:
        verbose_name='perfil'
        verbose_name_plural='perfiles'
        db_table='perfil'
        ordering=['id']


class ordenes(models.Model):
    comprador = models.CharField(max_length=20)
    cantidad = models.IntegerField()
    producto = models.ForeignKey(productos, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='ordenes'
        verbose_name_plural='ordenes'
        db_table='ordenes'
        ordering=['id']


class mensajes(models.Model):
    comprador = models.CharField(max_length=20)
    producto = models.ForeignKey(productos, on_delete=models.CASCADE)
    msg = models.CharField(max_length=350)
    rate = models.CharField(max_length=1)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='mensaje'
        verbose_name_plural='mensajes'
        db_table='mensaje'
        ordering=['id']


class ventas(models.Model):
    comprador = models.CharField(max_length=20)
    cantidad = models.IntegerField()
    producto = models.ForeignKey(productos, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    code_hash = models.CharField(max_length=250, default='none')
    code_t = models.CharField(max_length=50, default='none')
    sub_total = models.FloatField(default=0.0)
    iva = models.FloatField(default=0.0)
    total = models.FloatField(default=0.0)

    class Meta:
        verbose_name='ventas'
        verbose_name_plural='ventas'
        db_table='ventas'
        ordering=['id']
