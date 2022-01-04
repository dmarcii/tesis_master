from django.contrib import admin
from core.aplicacion1.models import *
from django.contrib.auth.admin import UserAdmin as OriginalUserAdmin
import os
import shutil
#from core.aplicacion1.models import *
# Register your models here.

class productos_display(admin.ModelAdmin):
    list_display = ('nombre', 'seccion', 'precio', 'imagen', 'stock', 'vendedor', 'vendidos')
    search_fields = ('nombre', 'seccion', 'precio', 'stock', 'vendedor', 'vendidos')
    list_filter = ('nombre', 'seccion', 'precio', 'stock', 'vendedor', 'vendidos')

class ordenes_display(admin.ModelAdmin):
    list_display = ('comprador', 'cantidad', 'producto', 'fecha')
    search_fields = ('comprador', 'cantidad', 'producto', 'fecha')
    list_filter = ('comprador', 'cantidad', 'producto', 'fecha')

class mensajes_display(admin.ModelAdmin):
    list_display = ('comprador', 'producto', 'msg', 'rate', 'fecha')
    search_fields = ('comprador', 'producto', 'msg', 'rate', 'fecha')
    list_filter = ('comprador', 'producto', 'msg', 'rate', 'fecha')


class perfiles_display(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'sexo', 'fecha_nacimiento', 'pais')
    search_fields = ('nombre', 'apellido', 'sexo', 'fecha_nacimiento', 'pais')
    list_filter = ('nombre', 'apellido', 'sexo', 'fecha_nacimiento', 'pais')


class ventas_display(admin.ModelAdmin):
    list_display = ('comprador', 'cantidad', 'producto', 'fecha', 'sub_total', 'iva', 'total')
    search_fields = ('comprador', 'cantidad', 'producto', 'fecha', 'sub_total', 'iva', 'total')
    list_filter = ('comprador', 'cantidad', 'producto', 'fecha', 'sub_total', 'iva', 'total')

def eliminar_perfil(modeladmin, request, queryset):

    for i in queryset:
        root = "C:/Users/danie/OneDrive/Escritorio/tesis/tesis_master/static/imagenes/perfiles/"+str(i.username)
        if os.path.exists(root):
            shutil.rmtree(root)

    queryset.delete()

class perfil_delete(OriginalUserAdmin):
    actions = [eliminar_perfil]



admin.site.unregister(User)
admin.site.register(User, perfil_delete)
admin.site.register(productos, productos_display)
admin.site.register(ordenes, ordenes_display)
admin.site.register(perfil_datos, perfiles_display)
admin.site.register(ventas, ventas_display)
admin.site.register(mensajes, mensajes_display)