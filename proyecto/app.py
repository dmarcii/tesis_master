from django.shortcuts import render, redirect
from django.http import HttpResponse
from proyecto.formUser import UserRegisterFrom
from core.aplicacion1.models import *
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from datetime import datetime
from django.contrib.auth.models import User
import os

class main(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = productos
    template_name = 'tienda_main.html'

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_queryset(self, **kwargs):

        if self.request.POST:
            date_insert = self.request.POST.get('search')
            return productos.objects.filter(nombre__icontains=date_insert)
        else:
            return productos.objects.all()

    def get_context_data(self, **kwargs):

        context = super(main, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        context['c_car'] = len(ordenes.objects.filter(comprador=self.request.user))
        return context


class pruebas_producto(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = productos
    template_name = 'tienda_product.html'

    def get_context_data(self, **kwargs):

        id = self.kwargs['id']
        producto = productos.objects.filter(id=id).first()
        context = super(pruebas_producto, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        context['c_car'] = len(ordenes.objects.filter(comprador=self.request.user))
        context['seller'] = producto.vendedor
        context['pr'] = producto
        context['name'] = str(producto.nombre)
        context['fotos'] = os.listdir(
            'C:/Users/Rosangel/PycharmProjects/ejemploDjango/proyecto/static/imagenes/perfiles/' + str(
                context['seller']) + '/' + str(producto.nombre))

        return context

def register(request):

    if request.method == 'POST':
        form = UserRegisterFrom(request.POST)

        if form.is_valid():

            form.save()

            perfil_datos.objects.create(nombre=request.POST.get('nombre'),
                                        apellido=request.POST.get('apellido'),
                                        sexo=request.POST.get('sexo'),
                                        fecha_nacimiento=request.POST.get('edad'),
                                        pais=request.POST.get('region'),
                                        usuario=User.objects.get(username=request.POST.get('username')))

            return redirect('/login')
    else:
        form = UserRegisterFrom()

    contex = {'form': form}
    return render(request, 'signup.html', contex)

@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/login')
def addcar(request, id):
    username = request.user
    cantidad = request.POST.get('quantity', False)

    if cantidad:
        pass
    else:
        cantidad = 1

    ordenes.objects.create(comprador=username,
                           cantidad=cantidad,
                           producto_id=id)
    return redirect('/car')