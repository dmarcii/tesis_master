from django import forms

class formventa(forms.Form):

    nombre = forms.CharField(max_length=20)
    seccion = forms.CharField(max_length=20)
    precio = forms.FloatField()
    descripccion = forms.CharField(max_length=200)
    detalles = forms.CharField(max_length=200)
    imagen1 = forms.ImageField()
    imagen2 = forms.ImageField(initial='x')
    imagen3 = forms.ImageField(initial='x')
    imagen4 = forms.ImageField(initial='x')
    stock = forms.IntegerField()