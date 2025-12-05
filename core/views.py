from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.contrib.auth.models import Group
from .models import Veiculo, Compra, StatusCredito
from .forms import (
    VeiculoForm,
    LoginForm,
    RegistroClienteForm,
    VeiculoFiltroForm,
    SaldoForm,
)
from django.contrib.auth import logout
from django.core.paginator import Paginator


# LOGIN LOGOUT REGISTRO


@login_required
def meu_perfil(request):
    user = request.user
    saldo_form = SaldoForm()
    comprados = Compra.objects.filter(cliente=user).select_related("veiculo")

    if request.method == "POST":
        saldo_form = SaldoForm(request.POST)
        if saldo_form.is_valid():
            novo_saldo = saldo_form.cleaned_data["saldo"]
            user.saldo = novo_saldo
            user.save()
            messages.success(
                request, f"Saldo atualizado para R$ {novo_saldo:.2f} com sucesso!"
            )
            return redirect("meu_perfil")

    return render(
        request,
        "perfil.html",
        {"user": user, "saldo_form": saldo_form, "comprados": comprados},
    )


def login_view(request):
    login_error = None
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            senha = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=senha)
            if user:
                login(request, user)
                messages.success(request, "Você entrou na sua conta")
                if user.has_perm("core.change_veiculo"):
                    return redirect("painel")
                return redirect("home")
            else:
                login_error = "Usuário ou senha inválidos."
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form, "login_error": login_error})


def logout_view(request):
    logout(request)
    return redirect("home")


def registrar_cliente(request):
    if request.method == "POST":
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            grupo, created = Group.objects.get_or_create(name="Cliente")
            user.groups.add(grupo)

            messages.success(
                request,
                f"Sua conta de Cliente foi criada com sucesso! Faça login para continuar.",
            )
            return redirect("login")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RegistroClienteForm()

    return render(request, "registro_usu.html", {"form": form})


# --- VEÍCULOS ---


def carros_listar(request):
    veiculos_comprados = Compra.objects.values_list("veiculo_id", flat=True)
    veiculos = Veiculo.objects.exclude(id__in=veiculos_comprados)
    form = VeiculoFiltroForm(request.GET)

    if form.is_valid():
        nome = form.cleaned_data.get("nome")
        ano_min = form.cleaned_data.get("ano_min")
        preco_max = form.cleaned_data.get("preco_max")
        quilometragem_max = form.cleaned_data.get("quilometragem_max")

        if nome:
            veiculos = veiculos.filter(nome__icontains=nome)

        if ano_min:
            veiculos = veiculos.filter(ano_modelo__gte=ano_min)

        if preco_max:
            veiculos = veiculos.filter(preco__lte=preco_max)

        if quilometragem_max:
            veiculos = veiculos.filter(quilometragem__lte=quilometragem_max)

    veiculos = veiculos.order_by("-ano_modelo", "preco")

    paginator = Paginator(veiculos, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "home.html", {"veiculos": page_obj, "form_filtro": form})


@login_required
@permission_required("core.add_veiculo", login_url="/login/")
def veiculo_criar(request):
    if request.method == "POST":
        form = VeiculoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Veículo criado com sucesso!")
            return redirect("painel")
        else:
            messages.error(request, "Erro ao criar veículo. Verifique os campos.")
    else:
        form = VeiculoForm()
    return render(request, "formveiculo.html", {"form": form})


@login_required
@permission_required("core.change_veiculo", login_url="/login/")
def veiculo_editar(request, id):
    veiculo = get_object_or_404(Veiculo, id=id)
    if request.method == "POST":
        form = VeiculoForm(request.POST, request.FILES, instance=veiculo)
        if form.is_valid():
            form.save()
            messages.success(request, "Veículo atualizado com sucesso!")
            return redirect("painel")
        else:
            messages.error(request, "Erro ao atualizar veículo.")
    else:
        form = VeiculoForm(instance=veiculo)
    return render(request, "formveiculo.html", {"form": form})


@login_required
@permission_required("core.delete_veiculo", login_url="/login/")
def veiculo_remover(request, id):
    veiculo = get_object_or_404(Veiculo, id=id)
    if request.method == "POST":
        veiculo.delete()
        messages.success(request, "Veículo removido com sucesso!")
        return redirect("painel")
    return render(request, "confirmar_remocao.html", {"veiculo": veiculo})


@login_required
def veiculos_infos(request, id):
    veiculo = get_object_or_404(Veiculo, id=id)

    if request.method == "POST":
        if request.user.saldo >= veiculo.preco:
            request.user.saldo -= veiculo.preco
            request.user.save()

            status_aprovado, created = StatusCredito.objects.get_or_create(
                nome_status="Aprovado"
            )
            Compra.objects.create(
                cliente=request.user, veiculo=veiculo, status_credito=status_aprovado
            )

            messages.success(
                request,
                f"Veículo {veiculo.nome} comprado com sucesso! Saldo restante: R$ {request.user.saldo:.2f}",
            )
            return redirect("home")
        else:
            messages.error(request, "Saldo insuficiente para comprar este veículo.")

    return render(request, "infos.html", {"veiculo": veiculo})


@login_required
@permission_required("core.change_veiculo", login_url="/login/")
def painel_vendedor(request):
    veiculos_comprados = Compra.objects.values_list("veiculo_id", flat=True)
    veiculos = Veiculo.objects.exclude(id__in=veiculos_comprados).order_by(
        "-ano_modelo", "preco"
    )
    form = VeiculoFiltroForm(request.GET)

    if form.is_valid():
        nome = form.cleaned_data.get("nome")
        ano_min = form.cleaned_data.get("ano_min")
        preco_max = form.cleaned_data.get("preco_max")
        quilometragem_max = form.cleaned_data.get("quilometragem_max")

        if nome:
            veiculos = veiculos.filter(nome__icontains=nome)

        if ano_min:
            veiculos = veiculos.filter(ano_modelo__gte=ano_min)

        if preco_max:
            veiculos = veiculos.filter(preco__lte=preco_max)

        if quilometragem_max:
            veiculos = veiculos.filter(quilometragem__lte=quilometragem_max)

    veiculos = veiculos.order_by("-ano_modelo", "preco")

    paginator = Paginator(veiculos, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "painel.html", {"veiculos": page_obj, "form_filtro": form})


@login_required
def deletar_conta(request):
    """
    View para deletar a conta do usuário autenticado
    """
    if request.method == "POST":
        user = request.user
        username = user.username
        user.delete()
        messages.success(request, f"Conta {username} foi deletada com sucesso!")
        return redirect("home")

    return render(request, "deletar_conta.html")
