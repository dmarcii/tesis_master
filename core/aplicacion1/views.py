from django.shortcuts import render, redirect
from django.views.generic import ListView
from core.aplicacion1.models import *
from core.aplicacion1.formularioVender import formventa
from core.aplicacion1.models import *
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
# Create your views here.

@login_required(login_url='/login')
def form_sell(request):

    if request.method == 'POST':

        miformulario = formventa(request.POST, files=request.FILES)

        if miformulario.is_valid():

            info = miformulario.cleaned_data

            username = request.user
            img = request.FILES['imagen']
            img_name = img.name

            upimage(img, str(username), img_name)

            productos.objects.create(nombre=info['nombre'],
                                     seccion=info['seccion'],
                                     precio=info['precio'],
                                     imagen=img_name,
                                     stock=info['stock'],
                                     vendedor=username)

            return redirect('/main')

    else:

        miformulario = formventa()

    return render(request, 'new.html', {'form':miformulario})

def upimage(file_image, user, image_name):

    ruta = 'C:/Users/Rosangel/PycharmProjects/ejemploDjango/proyecto/static/imagenes/perfiles'
    rutaUser = ruta + '/' + user + '/'

    if not os.path.exists(rutaUser):
        os.makedirs(rutaUser)

    fs = FileSystemStorage()
    fs.save(rutaUser + image_name, file_image)


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
    template_name = 'car.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        #a = ordenes.objects.filter(comprador=self.request.user) #.values('producto')
        #b = productos.objects.filter(pk__in=a)

        context = obtener_datos_carro(self.request.user)

        return context

@login_required(login_url='/login')
def eliminarCar(request, id):
    ordenes.objects.filter(comprador=request.user, id=id).delete()
    return redirect('/main/car')


@login_required(login_url='/login')
def buy(request, id):

    #falta eliminar la orden

    if request.method == 'POST':

        if id == '-1':

            context = obtener_datos_carro(request.user)

            hash_t = ''.join(random.choice('0123456789') for _ in range(10))

            nombre_qr = str(request.user) + str(codigo_seguridad_qe) + context['email'] + str(hash_t)

            hsh = _get_hashed_password(nombre_qr)

            hsh = hsh.replace('/', "slash")

            obj_qr = QR_CODE()

            obj_qr.crear_nuevo_qr(str(hsh), ("http://127.0.0.1:8000/main/factura/"+str(hsh)), str(request.user))

            for i in context['car']:
                ventas.objects.create(comprador=request.user,
                                       cantidad=i[1].cantidad,
                                       producto_id=i[0].id,
                                       code_hash=hsh,
                                       code_t = hash_t,
                                       sub_total=context['total'],
                                       iva=context['iva'],
                                       total=context['totaliva'])

            ordenes.objects.filter(comprador=request.user).delete()

            return redirect('/main/factura/'+hsh)

    return redirect('/main/car')


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
    context['email'] = user_email
    context['total'] = a[0].sub_total
    context['iva'] = a[0].iva
    context['totaliva'] = a[0].total

    return render(request, 'invoice.html', context)


def _get_hashed_password(password):
    return pbkdf2_sha256.encrypt(password, rounds=10, salt_size=10)

@login_required(login_url='/login')
def pruebas(request):

    obj = ordenes.objects.filter(comprador=request.user)

    #la contraseña especial + la fecha
    #nombre_qr = str(obj[0].comprador) + str(obj[0].fecha)

    #hsh = _get_hashed_password(nombre_qr)
    #hsh = hsh.replace('/', "slash")

    print(codigo_seguridad_qe)



    #obj_qr = QR_CODE()
    #obj_qr.crear_nuevo_qr(str(hsh), ("http://127.0.0.1:8000/main/factura/"+str(hsh)), str(request.user))


    #ordenes.objects.filter(comprador=request.user, id=id).delete()
    return redirect('/main')
