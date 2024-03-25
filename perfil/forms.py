from typing import Any
from django import forms
from . import models
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget= forms.PasswordInput(),
        label='Senha'
    )
    password2 = forms.CharField(
        required=False,
        widget= forms.PasswordInput(),
        label='Confirma Senha'
    )
    def __init__(self, usuario= None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario = usuario
        
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'password2', 'email')

    def clean(self, *args, **kwargs):
        validations_error_msgs = {}
        data = self.data
        cleaned = self.cleaned_data

        # variaveis de erros
        error_msg_user = 'Usuario ja existe'
        error_msg_email = 'Email ja existe'
        error_msg_password = 'Senha não confere'
        error_msg_password_short = 'Senha muito curta'
        error_msg_required = 'Este campo é obrigatório'

        # verificação de usuario
        usuario_data = cleaned.get('username')
        password_data = cleaned.get('password')
        password2_data = cleaned.get('password2')
        email_data = cleaned.get('email')

        usuario_db = User.objects.filter(username=usuario_data).first()
        email_db = User.objects.filter(email=email_data).first()

        if self.usuario:
            if usuario_db:
                if usuario_data != usuario_db.username:
                    validations_error_msgs['username'] = error_msg_user
            if email_db:
                if email_data != email_db.email:
                    validations_error_msgs['email'] = error_msg_email

            if password_data != password2_data:
                validations_error_msgs['password'] = error_msg_password
                validations_error_msgs['password2'] = error_msg_password

                if len(password_data) < 6:
                    validations_error_msgs['password2'] = error_msg_password_short
                    

        else:
            if usuario_db:
                validations_error_msgs['username'] = error_msg_user

            if email_db:
                validations_error_msgs['email'] = error_msg_email

            if not password_data:
                validations_error_msgs['password'] = error_msg_required
            if not password2_data:
                validations_error_msgs['password'] = error_msg_required

            if password_data != password2_data:
                validations_error_msgs['password'] = error_msg_password
                validations_error_msgs['password2'] = error_msg_password

            if len(password_data) < 6:
                validations_error_msgs['password2'] = error_msg_password_short           
        
        if validations_error_msgs:
            raise(forms.ValidationError(validations_error_msgs))

class PerfilForm(forms.ModelForm):
    class Meta:
        model = models.Perfil
        fields = '__all__'
        exclude = ('user', )


