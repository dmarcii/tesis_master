from django.db import models
from django.contrib.auth.models import User
from core.aplicacion1.models import *
# Create your models here.

class estados_productos(models.Model):
    comprador = models.CharField(max_length=20)
    code_t = models.CharField(max_length=50, default='none')
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.IntegerField()
    detalles = models.CharField(max_length=200)
    verficacion = models.BooleanField()

    class Meta:
        verbose_name='estados_producto'
        verbose_name_plural='estados_productos'
        db_table='estados_producto'
        ordering=['id']