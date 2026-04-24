from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_tables2 import SingleTableView

from .models import pessoa
from .tables import pessoa_table


def index(request):
    print("else")
    usuario = request.POST.get('username')
    senha = request.POST.get('password')
    user = authenticate(username=usuario, password=senha)
    if (user is not None):
        login(request, user)
        request.session['username'] = usuario
        request.session['password'] = senha
        request.session['usernamefull'] = user.get_full_name()
        print(request.session['username'])
        print(request.session['password'])
        print(request.session['usernamefull'])
        return redirect('pessoa_menu_alias')
    else:
        return render(request, 'index.html')

def logout_view(request):
    logout(request)
    return redirect('index_alias')

def pagina0(request):
    return render(request, 'pagina0.html')

def pagina1(request):
    return render(request, 'pagina1.html')

def pagina2(request):
    dictionary = {}
    registers = pessoa.objects.all()
    dictionary['pessoas'] = registers
    return render(request, 'pagina2.html', dictionary)

def pagina3(request):
    dicionario = {}
    registros = pessoa.objects.all()
    dicionario['pessoas'] = registros
    return render(request, 'pagina3.html', dicionario)

class pessoa_create(CreateView):
    model = pessoa
    fields = ['nome', 'email', 'fone', 'funcao', 'nascimento', 'ativo']
    def get_success_url(self):
        return reverse_lazy('pessoa_menu_alias')

class pessoa_list(SingleTableView):
    model = pessoa
    table_class = pessoa_table
    queryset = pessoa.objects.filter(ativo=True)

class pessoa_update(UpdateView):
    model = pessoa
    fields = ['nome', 'email', 'fone', 'funcao', 'nascimento', 'ativo']

    def get_success_url(self):
        return reverse_lazy('pessoa_menu_alias')

class pessoa_delete(DeleteView):
    model = pessoa
    success_url = reverse_lazy('pessoa_menu_alias')
    template_name = 'exemplo01/pessoa_delete.html' # Mantém por segurança caso o GET seja acessado

def pagina4(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        fone = request.POST.get('fone')
        funcao = request.POST.get('funcao')
        nascimento = request.POST.get('nascimento')
        ativo = request.POST.get('ativo')
        print("Nome:", nome)
        print("eMail:", email)
        print("Celular:", fone)
        print("Funcao:", funcao)
        print("Nascimento:", nascimento)
        print("ativo:", ativo)
    return render(request, 'pagina4.html')

class pessoa_menu(SingleTableView):
    model = pessoa
    table_class = pessoa_table
    template_name_suffix = '_menu'
    table_pagination = {"per_page": 5}
    template_name = 'exemplo01/pessoa_menu.html'
