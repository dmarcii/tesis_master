from django.db import models
from django.contrib.auth.models import User
from core.aplicacion1.models import *
import os
# Create your models here.

def path_file_name(instance, filename):
    ruta = 'C:/Users/Rosangel/PycharmProjects/ejemploDjango/proyecto/static/imagenes/imagenes_prodcutos/{0}'.format(instance.code_t)

    if not os.path.exists(ruta):
        os.makedirs(ruta)
    return 'C:/Users/Rosangel/PycharmProjects/ejemploDjango/proyecto/static/imagenes/imagenes_prodcutos/{0}/{1}'.format(instance.code_t, filename)

class estados_productos(models.Model):
    comprador = models.CharField(max_length=20)
    code_t = models.CharField(max_length=50, default='none')
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.IntegerField()
    detalles = models.CharField(max_length=200)
    verficacion = models.BooleanField()
    img1 = models.ImageField(upload_to=path_file_name, default='none', max_length=350)
    img2 = models.ImageField(upload_to=path_file_name, default='none', max_length=350)
    img3 = models.ImageField(upload_to=path_file_name, default='none', max_length=350)
    img4 = models.ImageField(upload_to=path_file_name, default='none', max_length=350)

    class Meta:
        verbose_name='estados_producto'
        verbose_name_plural='estados_productos'
        db_table='estados_producto'
        ordering=['id']