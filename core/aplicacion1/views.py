from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView
from core.aplicacion1.models import *
from core.aplicacion1.formularioVender import formventa
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
import os
from django.core.files.storage import FileSystemStorage
from passlib.hash import pbkdf2_sha256
from core.aplicacion1.codigo_qr import QR_CODE
from django.contrib.auth.models import User
from proyecto.settings import codigo_seguridad_qe
import random
from proyecto.app import *
from core.cede_app.models import *
from datetime import datetime
from django.core.paginator import Paginator
from django.views.generic import FormView

#from proyecto.formUser import *
# Create your views here.

@login_required(login_url='/login')
def form_sell(request):

    if request.method == 'POST':

        miformulario = formventa(request.POST, files=request.FILES)

        if miformulario.is_valid():

            lista = ['imagen1', 'imagen2', 'imagen3', 'imagen4']

            pr = []

            try:
                for i in lista:
                    img = request.FILES[i]
                    img_name = img.name
                    pr.append([img, img_name])
            except:
                pass

            upimage(pr, str(request.user), request.POST.get('nombre'))

            productos.objects.create(nombre=request.POST.get('nombre'),
                                     seccion=request.POST.get('seccion'),
                                     precio=request.POST.get('precio'),
                                     imagen=pr[0][1],
                                     stock=request.POST.get('stock'),
                                     vendedor=User.objects.get(username=request.user),
                                     descripccion=request.POST.get('descripccion'),
                                     detalles=request.POST.get('detalles'),
                                     vendidos=0)

            return redirect('/')

    else:
        miformulario = formventa()
    return render(request, 'new.html', {'form':miformulario})

def upimage(pr, user, nombre_producto):

    ruta = 'C:/Users/danie/OneDrive/Escritorio/tesis/tesis_master/static/imagenes/perfiles'
    rutaUser = ruta + '/' + user + '/' + nombre_producto + '/'

    if not os.path.exists(rutaUser):
        os.makedirs(rutaUser)

    fs = FileSystemStorage()
    for i in pr:
        fs.save(rutaUser + i[1], i[0])

def obtener_datos_carro(usuario):
    context = {}

    user = User.objects.get(username=usuario)
    user_email = user.email

    pr = []
    monto = 0

    for i in ordenes.objects.filter(comprador=usuario):
        producto = productos.objects.get(pk=i.producto_id)
        pr.append([producto, i])
        monto = monto + (int(producto.precio) * int(i.cantidad))

    iva = round(monto * 0.12, 2)
    total_iva = round(iva + monto, 2)

    context['car'] = pr
    context['email'] = user_email
    context['total'] = monto
    context['iva'] = iva
    context['totaliva'] = total_iva

    return context

class carrito(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = ordenes
    template_name = 'hijo_car.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        username = self.request.user

        #a = ordenes.objects.filter(comprador=self.request.user) #.values('producto')
        #b = productos.objects.filter(pk__in=a)

        context = obtener_datos_carro(username)
        context['c_car'] = len(ordenes.objects.filter(comprador=username))

        return context

@login_required(login_url='/login')
def eliminarCar(request, id):
    ordenes.objects.filter(comprador=request.user, id=id).delete()
    return redirect('/car')

@login_required(login_url='/login')
def buy(request, id):

    if request.method == 'POST':

        if id == '-1':

            context = obtener_datos_carro(request.user)

            hash_t = ''.join(random.choice('0123456789') for _ in range(10))

            nombre_qr = str(request.user) + str(codigo_seguridad_qe) + context['email'] + str(hash_t)

            hsh = _get_hashed_password(nombre_qr)

            hsh = hsh.replace('/', "slash")

            obj_qr = QR_CODE()
            obj_qr.crear_nuevo_qr(str(hsh), ("http://127.0.0.1:8000/factura/"+str(hsh)), str(request.user))

            for i in context['car']:

                ventas.objects.create(comprador=request.user,
                                       cantidad=i[1].cantidad,
                                       producto_id=i[0].id,
                                       code_hash=hsh,
                                       code_t = hash_t,
                                       sub_total=context['total'],
                                       iva=context['iva'],
                                       total=context['totaliva'])
                prv = i[0]
                prv.vendidos = int(prv.vendidos) + i[1].cantidad
                prv.save()

            estados_productos.objects.create(comprador=request.user,
                                   code_t = hash_t,
                                   estado=0,
                                   detalles='No verificado',
                                   verficacion=False)

            ordenes.objects.filter(comprador=request.user).delete()



            #productos.objects.create(comprador=self.request.user)

            return redirect('/factura/'+hsh)

    return redirect('/car')

@login_required(login_url='/login')
def show_invoice(request, id):

    a = ventas.objects.filter(comprador=request.user, code_hash = id)

    user = User.objects.get(username=request.user)
    user_email = user.email

    pr = []

    for i in a:
        pr.append([productos.objects.get(pk=i.producto_id), i.cantidad])

    context = {}

    context['car'] = pr
    context['hash'] = a[0].code_hash
    context['hash_t'] = a[0].code_t
    context['email'] = user_email
    context['total'] = a[0].sub_total
    context['iva'] = a[0].iva
    context['totaliva'] = a[0].total

    estado_obj = estados_productos.objects.get(code_t=a[0].code_t)

    valoraciones = ['Sin valoracion', 'Muy mal estado', 'En mal estado', 'Con detalles', 'En buen estado con pocos detalles', 'Perfecto estado']

    context['valoracion'] = valoraciones[estado_obj.estado]
    context['detalles'] = estado_obj.detalles

    if estado_obj.verficacion:
        context['verficacion'] = 'Verificado'
    else:
        context['verficacion'] = 'No verificado'

    return render(request, 'invoice.html', context)

def _get_hashed_password(password):
    return pbkdf2_sha256.encrypt(password, rounds=10, salt_size=10)

class list_all_invoices(LoginRequiredMixin, ListView):
    login_url = '/login/'
    template_name = 'list_invoces.html'

    def get_queryset(self, **kwargs):
        lista_facturas = ventas.objects.filter(comprador=self.request.user).values_list('code_hash', flat=True).distinct()
        lista_facturas = list(dict.fromkeys(lista_facturas))

        lista = []

        for i in lista_facturas:
            lista.append(ventas.objects.filter(comprador=self.request.user, code_hash=i).first())

        return lista

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['c_car'] = len(ordenes.objects.filter(comprador=self.request.user))

        return context

@login_required(login_url='/login')
def comentar(request,id):

    context = obtener_datos_carro(request.user)
    context['c_car'] = len(ordenes.objects.filter(comprador=request.user))

    mensajes.objects.create(comprador=request.user,
                          producto=productos.objects.get(id=id),
                          msg=request.POST.get('coment'),
                          rate=request.POST.get('rating'))

    return redirect('/producto/'+id)



'''class Formprueba(FormView):
    form_class = CategoryForm
    template_name = 'pruebaaas.html'
    success_url = '/pruebaaas3/'

    def form_valid(self, form):
        print(form.is_valid())
        print(form)
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.is_valid())
        print(form)
        return super().form_invalid(form)'''


@login_required(login_url='/login')
def pruebas(request):
    context = {}
    #print(request.COOKIES)
    #response = render(request, 'pruebaaas.html', context)
    #response.set_cookie('mikuki', 'hola mundo')
    #print(request.COOKIES)
    #return response

    '''p1 = Publication(title='The Python Journal')
    p1.save()
    p2 = Publication(title='Science News')
    p2.save()
    p3 = Publication(title='Science Weekly')
    p3.save()'''

    #a1 = Article(headline='Django holaaa')
    #a1.save()
    #a = Article.objects.all()
    b = Publication.objects.all()
    #a[0].publications.add(b[1])
    #print(a[0].publications.all())
    #print(a[1].publications.all())
    #print(a)

    if request.is_ajax():
        print('a')

    now = datetime.now()
    context['hora'] = now.strftime("%Y-%m-%d %H:%M:%S")

    #return render(request, 'editar_productos_hija.html', context)
    return render(request, 'pruebaaas.html', context)

@login_required(login_url='/login')
def pruebas2(request):
    context = {}
    pr = productos.objects.all()
    context['productos'] = pr
    #now = datetime.now()
    #context['hora'] = now.strftime("%Y-%m-%d %H:%M:%S")
    #context['paper'] = productos.objects.all()[0]
    #print(JsonResponse(context, safe=True))

    return render(request, 'pruebajax.html', context)

    #return JsonResponse(context, safe=False)


class list_store(ListView):

    template_name = 'tienda_store.html'

    def dispatch(self, request, *args, **kwargs):

        if request.method == 'GET':
            self.date_insert = self.request.GET.get('busquedad')
            self.minimo = self.request.GET.get('minimo')
            self.maximo = self.request.GET.get('maximo')

            if self.maximo == 'ind':
                self.obj = productos.objects.filter(nombre__icontains=self.date_insert,
                                                    precio__gte=self.minimo,)
            else:
                self.obj = productos.objects.filter(nombre__icontains=self.date_insert,
                                               precio__lte=self.maximo,
                                               precio__gte=self.minimo,)

            self.page = self.request.GET.get('page')
            return self.get(request, *args, **kwargs)

        elif request.method == 'POST':
            return self.get(request, *args, **kwargs)

    def get_queryset(self, **kwargs):

        p = Paginator(self.obj, 3)

        if self.page == None:
            self.page = 1

        self.paginacion = p.get_page(self.page)

        obj = p.page(self.page).object_list

        reputaciones = []

        for i in obj:
            reputaciones.append(reputacion(i, opc='no')['promedio'])

        return list(zip(obj, reputaciones))

        '''try:
        except Exception as e:
            pass'''

    def get_context_data(self, **kwargs):

        context = super(list_store, self).get_context_data(**kwargs)

        context['paginas'] = self.paginacion
        context['c_car'] = len(ordenes.objects.filter(comprador=self.request.user))
        context['max'] = self.maximo
        context['min'] = self.minimo
        context['search'] = self.date_insert
        return context


class edit(LoginRequiredMixin, ListView):
    login_url = '/login/'
    template_name = 'editar_productos_hija.html'

    def get_queryset(self, **kwargs):

        return productos.objects.filter(vendedor=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['c_car'] = len(ordenes.objects.filter(comprador=self.request.user))

        return context



class edit(LoginRequiredMixin, ListView):
    login_url = '/login/'
    template_name = 'editar_productos_hija.html'

    def get_queryset(self, **kwargs):
        return productos.objects.filter(vendedor=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['c_car'] = len(ordenes.objects.filter(comprador=self.request.user))

        return context

@login_required(login_url='/login')
def eliminarProducto(request, id):
    productos.objects.filter(vendedor=request.user, id=id).delete()
    return redirect('/editar')