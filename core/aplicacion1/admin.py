from django.contrib import admin
from core.aplicacion1.models import *
# Register your models here.

class productos_display(admin.ModelAdmin):
    list_display = ('nombre', 'seccion', 'precio', 'imagen', 'stock', 'vendedor')
    search_fields = ('nombre', 'seccion', 'precio', 'imagen', 'stock', 'vendedor')
    list_filter = ('nombre', 'seccion', 'precio', 'imagen', 'stock', 'vendedor')

class ordenes_display(admin.ModelAdmin):
    list_display = ('comprador', 'cantidad', 'producto', 'fecha')
    search_fields = ('comprador', 'cantidad', 'producto', 'fecha')
    list_filter = ('comprador', 'cantidad', 'producto', 'fecha')

#('comprador', 'cantidad', 'producto', 'fecha', 'code_hash')

admin.site.register(productos, productos_display)
admin.site.register(ordenes, ordenes_display)