from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterFrom(UserCreationForm):
    username = forms.CharField(label='Usuario', max_length=20, widget=forms.TextInput(attrs={'class': 'user', 'onkeyup':'feedback_form_control()'}))
    edad = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'user', 'onkeyup':'feedback_form_control()'}))
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'pass1', 'onkeyup':'feedback_form_control()'}))
    password2 = forms.CharField(label='Confirma contraseña', widget=forms.PasswordInput(attrs={'class': 'pass2', 'onkeyup':'feedback_form_control()'}))
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {k: "" for k in fields}