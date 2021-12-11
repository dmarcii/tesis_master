from django.urls import path
from core.aplicacion1.views import *

app_name = 'aplicacion1'
#/checkout/all
urlpatterns = [
    path('sell/', form_sell, name='vender'),
    path('car/', carrito.as_view(), name='carrito'),
    path('car/cardelete/<int:id>', eliminarCar, name='eliminar'),
    path('car/buy/<str:id>', buy, name='comprar'),
    path('factura/<str:id>', show_invoice, name='factura'),
    path('facturas/', list_all_invoices.as_view(), name='facturas'),
    path('comentar/<str:id>', comentar, name='comentar'),
    path('busquedad/', list_store.as_view(), name='prueba'),
    path('editar/', edit.as_view(), name='prueba'),
    path('del/<int:id>', eliminarProducto, name='eliminar'),
    path('pruebaaas/', pruebas),

]