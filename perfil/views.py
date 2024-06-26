from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.base import View
from django.contrib.auth.models import User
import copy
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from . import models
from . import forms


class BasePerfil(View):
    template_name = 'perfil/criar.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.carrinho = copy.deepcopy(self.request.session.get('carrinho, {}'))

        self.perfil = None
        if self.request.user.is_authenticated:
            self.perfil = models.Perfil.objects.filter(user=self.request.user).first()
            self.contexto = {
                'userform': forms.UserForm(data=self.request.POST or None,
                                           usuario=self.request.user,
                                           instance=self.request.user),
                'perfilform': forms.PerfilForm(data=self.request.POST or None, instance=self.perfil) 
            }
        else:
            self.contexto = {
                'userform': forms.UserForm(data=self.request.POST or None),
                'perfilform': forms.PerfilForm(data=self.request.POST or None) 
            }
        
        self.userform = forms.UserForm(data=self.request.POST or None)
        self.perfilform = forms.PerfilForm(data=self.request.POST or None)

        if self.request.user.is_authenticated:
            self.template_name = 'perfil/atualizar.html' 

        self.rendenizar = render(self.request,self.template_name, self.contexto)

        return self.rendenizar

    def get(self, *args, **kwargs):
        return self.rendenizar


class Criar(BasePerfil):
    def post(self, *args, **kwargs):
        if not self.perfilform.is_valid() or not self.userform.is_valid():
            return self.rendenizar
        
        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password')
        email = self.userform.cleaned_data.get('email')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')


        if self.request.user.is_authenticated:
            usuario = get_object_or_404(User, username=self.request.user.username)
            usuario.username = username

            if password:
                usuario.set_password(password)

            usuario.email = email
            usuario.first_name = first_name
            usuario.last_name = last_name
            usuario.save()

            # se não existir perfil cria um novo
            if not self.perfil:
                self.perfilform.cleaned_data['usuario'] = usuario
                perfil = models.Perfil(**self.perfilform.cleaned_data)
                perfil.save()
            else:
                perfil = self.perfilform.save(commit=False)
                perfil.user = usuario
                perfil.save()
        else:
            usuario = self.userform.save(commit=False)
            usuario.set_password(password) # criptografando a senha
            usuario.save()

            perfil = self.perfilform.save(commit=False)
            perfil.user = usuario
            perfil.save()

        # loga o usuario novamente ao alterar os dados do cadastro
        if password:
            autentica = authenticate(
                self.request,
                user=usuario,
                password=password
            )

            if autentica:
                login(self.request,user=autentica)
            
        self.request.session['carrinho'] = self.carrinho
        self.request.session.save()

        messages.success(self.request, "Cadastro Concluido com sucesso!")
        return redirect('perfil:criar')
        # return self.rendenizar

class Atualizar(BasePerfil):
    def get(self,*args, **kwargs):
        return HttpResponse('atualizar')

class Logout(View):
    def get(self,*args, **kwargs):
        carrinho = copy.deepcopy(self.request.session.get('carrinho'))
        logout(self.request)
        self.request.session['carrinho'] = carrinho
        self.request.session.save()
        return redirect('perfil:criar')

class Login(View):
    def post(self,*args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        if not username or not password:
            messages.error(self.request, 'Usuario ou senha Incorreto.')
            return redirect('perfil:criar')
        
        usuario = authenticate(self.request, username=username, password=password)

        if not usuario:
            messages.error(self.request, 'Usuario ou senha Incorreto.')
            return redirect('perfil:criar')
        
        login(self.request, usuario)
        return redirect('produto:carrinho')
