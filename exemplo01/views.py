from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_tables2 import SingleTableView
from django.core.files.storage import FileSystemStorage
from plotly.offline import plot

from .models import pessoa
from .forms import PessoaForm
from .tables import pessoa_table
from .models import exame

import plotly.graph_objs as go

class PermissionRequiredGenericMixin:
    """
    Mixin genérico para verificação de permissão em Class-Based Views.

    Uso:
        class MinhaView(PermissionRequiredGenericMixin, ListView):
            permission_required = 'app_label.codename'
            permission_denied_message = 'Mensagem personalizada'  # opcional
    """
    permission_required = None
    permission_denied_message = "Você não tem permissão para acessar esta página."

    def dispatch(self, request, *args, **kwargs):
        if self.permission_required and request.user.has_perm(self.permission_required):
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponse(self.permission_denied_message)


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

class pessoa_list(PermissionRequiredGenericMixin, SingleTableView):
    permission_required = "exemplo01.view_pessoa"
    permission_denied_message = "Sem permissão para listar pessoas"
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

def pagina5(request):
    if request.method == 'POST':
        form = PessoaForm(request.POST)
        if form.is_valid():
            xnome = form.cleaned_data['nome']
            xemail = form.cleaned_data['email']
            xfone = form.cleaned_data['fone']
            xfuncao = form.cleaned_data['funcao']
            xnascimento = form.cleaned_data['nascimento']
            xativo = form.cleaned_data['ativo']
            print("Nome:", xnome)
            print("eMail:", xemail)
            print("Celular:", xfone)
            print("Funcao:", xfuncao)
            print("Nascimento:", xnascimento)
            print("ativo:", xativo)
            pessoa.objects.create(nome=xnome, email=xemail, fone=xfone,
                                  funcao=xfuncao, nascimento=xnascimento, ativo=xativo)
            form = PessoaForm()
    else:
        form = PessoaForm()
    return render(request, 'pagina5.html', {'form': form})

def pagina6(request):
    dicionario = {}
    registros = pessoa.objects.all()
    dicionario['pessoas'] = registros
    return render(request, 'pagina6.html', dicionario)


def pagina11(request):
    import os
    if request.method == 'POST' and request.FILES['arq_upload']:
        fss = FileSystemStorage()
        upload = request.FILES['arq_upload']
        file1 = fss.save(upload.name, upload)
        file_url = fss.url(file1)

        print("upload", upload)
        print("file1", file1)
        print("file_url", file_url)

        file2 = open(file1, 'r')
        for row in file2:
            colunas = row.replace("(", "").replace(")", "").split(",")
            exame.objects.create(valor=float(colunas[8]))
        file2.close()
        os.remove(file_url.replace("/", ""))
        return HttpResponse("Arquivo Importado")
    return render(request, 'pagina11.html')

def pagina12(request):
    exame_tmp = exame.objects.all()
    eixo_x = []
    eixo_y = []
    i = 0
    for e in exame_tmp:
        i += 1
        eixo_x.append(i)
        eixo_y.append(e.valor)
    figura = go.Figure()
    figura.add_trace(go.Scatter(x=eixo_x, y=eixo_y, mode='lines', line_color='rgb(0, 0, 255)'))
    figura.update_layout(title="Dados de Exame", title_x=0.5, xaxis_title='Tempo', yaxis_title='Batimento Cardíaco')
    plot_div = plot(figura, output_type='div')
    dicionario = {}
    dicionario['grafico'] = plot_div
    return render(request, 'pagina12.html', dicionario)

class pessoa_menu(SingleTableView):
    model = pessoa
    table_class = pessoa_table
    template_name_suffix = '_menu'
    table_pagination = {"per_page": 5}
    template_name = 'exemplo01/pessoa_menu.html'
