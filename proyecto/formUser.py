from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import datetime
from core.aplicacion1.models import *

class UserRegisterFrom(UserCreationForm):
    username = forms.CharField(label='Usuario', max_length=20, widget=forms.TextInput(attrs={'class': 'user', 'onkeyup':'feedback_form_control()'}))
    nombre = forms.CharField(label='Nombre', max_length=20, widget=forms.TextInput(attrs={'class': 'user', 'onkeyup':'feedback_form_control()'}))
    apellido = forms.CharField(label='apellido', max_length=20, widget=forms.TextInput(attrs={'class': 'user', 'onkeyup': 'feedback_form_control()'}))
    edad = forms.DateField(widget=forms.TextInput(attrs={'class': 'user', 'onkeyup':'feedback_form_control()', 'type': 'date'}))
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'pass1', 'onkeyup':'feedback_form_control()'}))
    password2 = forms.CharField(label='Confirma contraseña', widget=forms.PasswordInput(attrs={'class': 'pass2', 'onkeyup':'feedback_form_control()'}))
    sexo = forms.ChoiceField(choices=[('Masculino', 'Masculino'),
                                      ('Femenino', 'Femenino')])
    email = forms.EmailField()

    def clean_edad(self):
        birthdate = self.cleaned_data['edad']
        today = datetime.date.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

        if age < 18:
            raise forms.ValidationError('Must be at least 18 years old to register')
        return birthdate

    class Meta:
        model = User
        fields = ['username', 'nombre', 'sexo', 'apellido', 'email', 'edad', 'password1', 'password2']
        #help_texts = {k: "" for k in fields}



'''class CategoryForm(forms.ModelForm):

    class Meta:
        model = perfil_datos
        fields = '__all__'''