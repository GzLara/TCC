from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class UsuarioForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, label="Nome")
    last_name = forms.CharField(max_length=50, required=True, label="Sobrenome")
    email = forms.EmailField(max_length=100, required=True, help_text='Obrigatório. Informe um endereço de e-mail válido.')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("O e-mail {} já está em uso.".format(email))
        
        return email
