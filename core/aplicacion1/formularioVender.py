from django import forms

class formventa(forms.Form):

    nombre = forms.CharField(max_length=20)
    seccion = forms.CharField(max_length=20)
    precio = forms.FloatField()
    imagen1 = forms.ImageField()
    imagen2 = forms.ImageField(initial='x')
    imagen3 = forms.ImageField(initial='x')
    imagen4 = forms.ImageField(initial='x')
    stock = forms.IntegerField()