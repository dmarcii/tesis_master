from django import forms

class formventa(forms.Form):

    nombre = forms.CharField(max_length=20)
    seccion = forms.CharField(max_length=20)
    precio = forms.FloatField()
    imagen = forms.ImageField()
    stock = forms.IntegerField()