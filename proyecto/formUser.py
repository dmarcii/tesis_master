from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import datetime

class UserRegisterFrom(UserCreationForm):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "", "aria-label": "First name", 'onkeyup':'feedback_form_control()'}))
    nombre = forms.CharField(label='Nombre', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "", "aria-label": "First name",  'onkeyup':'feedback_form_control()'}))
    apellido = forms.CharField(label='apellido', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "", "aria-label": "Apellido", 'onkeyup': 'feedback_form_control()'}))
    email = forms.EmailField(label='email', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "", "aria-label": "Correo Electrónico", 'onkeyup': 'feedback_form_control()'}))
    edad = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "Edad", "aria-label": "Edad", 'onkeyup':'feedback_form_control()', 'type': 'date'}))
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control', 'onkeyup':'feedback_form_control()'}))
    password2 = forms.CharField(label='Confirma contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control', 'onkeyup':'feedback_form_control()'}))
    sexo = forms.ChoiceField(choices=[('Masculino', 'Masculino'),
                                      ('Femenino', 'Femenino')])
    def clean_edad(self):
        birthdate = self.cleaned_data['edad']
        today = datetime.date.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        if age < 18:
            raise forms.ValidationError('Debes tener mas de 18 años para poder registrarte')
        return birthdate
    class Meta:
        model = User
        fields = ['username', 'nombre', 'sexo', 'apellido', 'email', 'edad', 'password1', 'password2']
        #help_texts = {k: "" for k in fields}