from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View

app_name = 'perfil'

class Criar(View):
    def get(self,*args, **kwargs):
        return HttpResponse('Criar')

class Atualizar(View):
    def get(self,*args, **kwargs):
        return HttpResponse('Atualizar')

class Logout(View):
    def get(self,*args, **kwargs):
        return HttpResponse('Logout')

class Login(View):
    def get(self,*args, **kwargs):
        return HttpResponse('Login')
