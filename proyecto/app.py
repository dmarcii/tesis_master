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
from collections import Counter
from django.views import View
from django.views.generic import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
import os#

class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.success_url)

class main(ListView):
    model = productos
    template_name = 'tienda_main.html'

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_queryset(self, **kwargs):

        reputaciones = []

        for i in productos.objects.all():
            reputaciones.append(reputacion(i, opc='no')['promedio'])

        return list(zip(productos.objects.all(), reputaciones))

    def get_context_data(self, **kwargs):
        context = super(main, self).get_context_data(**kwargs)
        context['c_car'] = len(ordenes.objects.filter(comprador=self.request.user))

        reputaciones = []

        list_top = productos.objects.all().order_by('-vendidos')[:10]

        for i in list_top:
            reputaciones.append(reputacion(i, opc='no')['promedio'])

        top_vendidos = list(zip(list_top, reputaciones))

        context['top_sell'] = top_vendidos

        return context

class pruebas_producto(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = productos
    template_name = 'tienda_product.html'

    def get_queryset(self, **kwargs):

        id = self.kwargs['id']
        producto = productos.objects.filter(id=id).first()
        return mensajes.objects.filter(producto=producto)

    def get_context_data(self, **kwargs):

        id = self.kwargs['id']
        producto = productos.objects.filter(id=id).first()
        context = super(pruebas_producto, self).get_context_data(**kwargs)
        context['c_car'] = len(ordenes.objects.filter(comprador=self.request.user))
        context['seller'] = producto.vendedor
        context['c_reviews'] = len(mensajes.objects.filter(producto=producto))
        context['id_producto'] = producto.id
        context['pr'] = producto
        context['name'] = str(producto.nombre)
        context['fotos'] = os.listdir(
            'C:/Users/Rosangel/PycharmProjects/ejemploDjango/proyecto/static/imagenes/perfiles/' + str(
                context['seller']) + '/' + str(producto.nombre))

        c = reputacion(producto)

        context.update(c)
        return context

def reputacion(producto, opc='todo'):

    lista_facturas = mensajes.objects.filter(producto=producto).values_list('rate', flat=True)
    a = dict(Counter(lista_facturas))

    cont1 = 0

    c = {}

    #print(list(map(int, lista_facturas)))

    for i in a:
        cont1 += (a[i]) * int(i)

    if len(lista_facturas) == 0:
        c['promedio'] = 0
    else:
        c['promedio'] = round(cont1 / len(lista_facturas), 2)


    if opc == 'todo':

        b = {}

        for i in a:
            b[i] = int((a[i] / len(lista_facturas)) * 100)

        for i in ['0', '1', '2', '3', '4', '5']:
            try:
                if b[i]:
                    pass
            except:
                b[i] = 0

        nombres = ['estrella0', 'estrella1', 'estrella2', 'estrella3', 'estrella4', 'estrella5']
        for i, j in enumerate(nombres):
            try:
                c[j] = [b[str(i)], a[str(i)]]
            except:
                c[j] = [b[str(i)], 0]

    return c

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

