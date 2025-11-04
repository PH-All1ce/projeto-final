from django.shortcuts import render, redirect, get_object_or_404,redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from .models import Veiculo
from .forms import VeiculoForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .forms import LoginForm 

def carros_listar(request):
    veiculos = Veiculo.objects.all()
    context = {'veiculos': veiculos}
    return render(request, "home.html", context)

def logout_view(request):
    logout(request)
    return redirect('login')

def painel_vendedor(request):
    if request.session.get("tipo") == "vendedor":
        veiculos = Veiculo.objects.all()
        return render(request, "painel.html", {"veiculos": veiculos})
    return redirect("listar")

def veiculos_listar_remover(request):
    veiculos = Veiculo.objects.all()
    return render(request, 'removeveiculo.html', {'veiculos': veiculos})

def veiculo_remover(request, id):
    veiculo = get_object_or_404(Veiculo, id=id)
    veiculo.delete()
    return redirect('home')

def veiculos_infos(request, id):
    veiculo = get_object_or_404(Veiculo, id=id)
    return render(request, 'infos.html', {'veiculo': veiculo})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            senha = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=senha)
            if user is not None:
                login(request, user)

                if user.has_perm('sua_app.change_veiculo'): 
                    return redirect('painel_vendedor')
                return redirect('home')
            else:
                messages.error(request, "E-mail ou senha inválidos.")
    else:
        form = LoginForm()
    
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request) 
    return redirect('home')

@login_required
@permission_required('sua_app.change_veiculo', login_url='/login/') 
def painel_vendedor(request):
    veiculos = Veiculo.objects.all()
    return render(request, "painel.html", {"veiculos": veiculos})


@login_required
@permission_required('sua_app.add_veiculo', login_url='/login/') 
def veiculo_criar(request):
    if request.method == 'POST':
        form = VeiculoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = VeiculoForm()
    return render(request, "formveiculo.html", {'form': form})

    return render(request, "formveiculo.html", {'form': form})

def registrar_cliente(request):
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            tipo = form.cleaned_data['tipo_usuario']
            user.save()
            grupo = Group.objects.get(name=tipo)
            user.groups.add(grupo)
            return redirect('base')
    else:
        form = RegistroClienteForm()
    return render(request, 'registro_usu.html', {'form': form})

@login_required
@permission_required('sua_app.change_veiculo', login_url='/login/') 
def veiculo_editar(request, id):
    veiculo = get_object_or_404(Veiculo, id=id)
    if request.method == 'POST':
        form = VeiculoForm(request.POST, request.FILES, instance=veiculo)
        if form.is_valid():
            form.save()
            return redirect('painel_vendedor') 
    else:
        form = VeiculoForm(instance=veiculo)
    return render(request, 'formveiculo.html', {'form': form})


@login_required
@permission_required('sua_app.delete_veiculo', login_url='/login/') 
def veiculo_remover(request, id):
    veiculo = get_object_or_404(Veiculo, id=id)
    if request.method == 'POST': 
        veiculo.delete()
        return redirect('painel_vendedor')
    return render(request, 'confirmar_remocao.html', {'veiculo': veiculo})
