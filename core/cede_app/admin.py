from django.contrib import admin
from core.cede_app.models import *
# Register your models here.

class estados_display(admin.ModelAdmin):
    list_display = ('comprador', 'code_t', 'fecha', 'estado', 'detalles', 'verficacion', 'img1', 'img2', 'img3', 'img4')
    search_fields = ('comprador', 'code_t', 'fecha', 'estado', 'detalles', 'verficacion')
    list_filter = ('comprador', 'code_t', 'fecha', 'estado', 'detalles', 'verficacion')
    list_editable = ('estado', 'detalles', 'verficacion', 'img1', 'img2', 'img3', 'img4')

admin.site.register(estados_productos, estados_display)
