from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)  # renderizar templates | redirecionar para URLs | buscar objetos ou erro
from django.contrib.auth import (
    authenticate,
    login,
    logout,
)  # verificar se tem permissão | iniciar e encerrar sessão
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
)  # restringe o acesso as views para logados | com permissão especifica
from django.contrib import (
    messages,
)  # framework de mensagem (sucesso ou erro para o usuário)
from django.contrib.auth.models import Group  # gerenciar grupos de usuários
from .models import Veiculo, Compra, StatusCredito
from .forms import (
    VeiculoForm,
    LoginForm,
    RegistroClienteForm,
    VeiculoFiltroForm,
    SaldoForm,
    PerfilEditForm,
)
from django.contrib.auth import logout
from django.core.paginator import Paginator  # paginação

# recebe as requisições, define a lógica da resposta e devolve as respostas adequadas

# LOGIN LOGOUT REGISTRO EDITAR PERFIL


@login_required  # verifica se está logado
def meu_perfil(request):
    user = request.user
    saldo_form = SaldoForm()  # recebe os dados do formulário
    comprados = Compra.objects.filter(cliente=user).select_related(
        "veiculo"
    )  # veículos comprados pelo usuário

    if request.method == "POST":
        saldo_form = SaldoForm(
            request.POST
        )  # post "postar" dados, dados não são enviadas pelo url, mas pelo corpo da requisição
        if saldo_form.is_valid():  # valida os dados
            novo_saldo = saldo_form.cleaned_data["saldo"]  # extrai o valor
            user.saldo = novo_saldo  # atualiza o atributo
            user.save()  # salva no banco de dados
            messages.success(
                request, f"Saldo atualizado para R$ {novo_saldo:.2f} com sucesso!"
            )
            return redirect("meu_perfil")  # recarrega a página

    return render(
        request,
        "perfil.html",
        {"user": user, "saldo_form": saldo_form, "comprados": comprados},
    )  # renderiazar o template com os dados do usuário


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
                if user.has_perm(
                    "core.change_veiculo"
                ):  # se tiver permissão de vendedor, libera o painel
                    return redirect("painel")
                return redirect(
                    "home"
                )  # se for cliente, redireciona para o menu principal
            else:
                login_error = "Usuário ou senha inválidos."
    else:  # se for método get, apenas carrega o menu de login vazio
        form = LoginForm()
    return render(request, "login.html", {"form": form, "login_error": login_error})


def logout_view(
    request,
):  # encerra sessão
    logout(request)
    return redirect("home")


def registrar_cliente(request):
    if request.method == "POST":
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            grupo, created = Group.objects.get_or_create(
                name="Cliente"
            )  # usuário é adicionado ao grupo cliente (vendedor só pode ser promovido pelo dono)
            user.groups.add(grupo)

            messages.success(
                request,
                f"Sua conta de Cliente foi criada com sucesso! Faça login para continuar.",
            )
            return redirect(
                "login"
            )  # se registrar, o usuário é redirecionado para o login
        else:  # se o form não for válido, exibe mensagem de erro nos campos errados
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:  # se for GET, exibe o template para criar a conta
        form = RegistroClienteForm()

    return render(request, "registro_usu.html", {"form": form})


@login_required
def editar_perfil(request):
    user = request.user
    if request.method == "POST":
        form = PerfilEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso.")
            return redirect("meu_perfil")
    else:  # se for GET, carrega o formulário com os dados atuais do usuário
        form = PerfilEditForm(instance=user)
    return render(request, "editar_perfil.html", {"form": form})


# VEÍCULOS


def carros_listar(request):
    veiculos_comprados = Compra.objects.values_list(
        "veiculo_id", flat=True
    )  # busca todos os veículos que foram comprados
    veiculos = Veiculo.objects.exclude(
        id__in=veiculos_comprados
    )  # exclui os veículos que já foram comprados e mostra só os disponíveis
    form = VeiculoFiltroForm(request.GET)

    if (
        form.is_valid()
    ):  # se o formulário for preenchido corretamente vai filtrar de acordo com o atributo escolhido
        nome = form.cleaned_data.get("nome")
        ano_min = form.cleaned_data.get("ano_min")
        preco_max = form.cleaned_data.get("preco_max")
        quilometragem_max = form.cleaned_data.get("quilometragem_max")

        if nome:
            veiculos = veiculos.filter(
                nome__icontains=nome
            )  # se for preenchido, busca os veículos com o nome ou parte desse nome. (incontains)

        if ano_min:
            veiculos = veiculos.filter(ano_modelo__gte=ano_min)

        if preco_max:
            veiculos = veiculos.filter(preco__lte=preco_max)

        if quilometragem_max:
            veiculos = veiculos.filter(quilometragem__lte=quilometragem_max)

    veiculos = veiculos.order_by(
        "-ano_modelo", "preco"
    )  # ordena a listagem de acordo com o ano (mais novo) e o preço (mais barato)

    paginator = Paginator(veiculos, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)  # mostra o objeto de acordo com a página

    return render(
        request, "home.html", {"veiculos": page_obj, "form_filtro": form}
    )  # renderiza o home com os veículos de cada página e o filtro


@login_required
@permission_required(
    "core.add_veiculo", login_url="/login/"
)  # requere permissão (do django admin), se não tiver vai para o login
def veiculo_criar(request):
    if request.method == "POST":
        form = VeiculoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Veículo criado com sucesso!")
            return redirect("painel")
        else:
            messages.error(request, "Erro ao criar veículo. Verifique os campos.")
    else:  # se GET, motra o formulário vazio, para criar o veículo
        form = VeiculoForm()
    return render(request, "formveiculo.html", {"form": form})


@login_required
@permission_required(
    "core.change_veiculo", login_url="/login/"
)  # exige permissão de editar o veículo, se não tiver manda para o login
def veiculo_editar(request, id):
    veiculo = get_object_or_404(Veiculo, id=id)  # procura o veículo ou retorna um erro
    if request.method == "POST":
        form = VeiculoForm(request.POST, request.FILES, instance=veiculo)
        if (
            form.is_valid()
        ):  # se estiver correto, salva, manda a mensagem de sucesso e redireciona para o painel
            form.save()
            messages.success(request, "Veículo atualizado com sucesso!")
            return redirect("painel")
        else:
            messages.error(request, "Erro ao atualizar veículo.")
    else:  # se for GET, cria uma instancia com os dados atuais
        form = VeiculoForm(instance=veiculo)
    return render(request, "formveiculo.html", {"form": form})


@login_required
@permission_required(
    "core.delete_veiculo", login_url="/login/"
)  # só pode ser utilizado se tiver permissão de deletar (do admin), ou vai para login
def veiculo_remover(request, id):
    veiculo = get_object_or_404(Veiculo, id=id)  # busca o objeto ou retorna o erro
    if (
        request.method == "POST"
    ):  # se for post, deleta o veículo, da mensagem de confirmação e redireciona para o painel
        veiculo.delete()
        messages.success(request, "Veículo removido com sucesso!")
        return redirect("painel")
    return render(
        request, "confirmar_remocao.html", {"veiculo": veiculo}
    )  # se for GET pede para o usuário confirmar a remoção


@login_required
def veiculos_infos(request, id):
    veiculo = get_object_or_404(Veiculo, id=id)

    if request.method == "POST":
        if (
            request.user.saldo >= veiculo.preco
        ):  # verifica se da para comprar o veic com o saldo
            request.user.saldo -= veiculo.preco  # subtrai o preço do veic do saldo
            request.user.save()  # atualiza o novo saldo

            status_aprovado, created = StatusCredito.objects.get_or_create(
                nome_status="Aprovado"
            )
            Compra.objects.create(  # cria um novo registro na tabela de compra, ligando o cliente ao veic
                cliente=request.user, veiculo=veiculo, status_credito=status_aprovado
            )

            messages.success(
                request,
                f"Veículo {veiculo.nome} comprado com sucesso! Saldo restante: R$ {request.user.saldo:.2f}",
            )
            return redirect("home")
        else:
            messages.error(request, "Saldo insuficiente para comprar este veículo.")
    # se for um GET ou der erro de saldo, apenas mostra a informação do veículo
    return render(request, "infos.html", {"veiculo": veiculo})


@login_required
@permission_required("core.change_veiculo", login_url="/login/")
def painel_vendedor(request):
    veiculos_comprados = Compra.objects.values_list(
        "veiculo_id", flat=True
    )  # busca todos os veículos que já foram comprados
    veiculos = Veiculo.objects.exclude(id__in=veiculos_comprados).order_by(
        "-ano_modelo", "preco"
    )  # exclui os veículos que já foram comprados e mostra só os disponíveis
    form = VeiculoFiltroForm(request.GET)

    if (
        form.is_valid()
    ):  # se o formulário for preenchido corretamente vai filtrar de acordo com o escolhido
        nome = form.cleaned_data.get("nome")
        ano_min = form.cleaned_data.get("ano_min")
        preco_max = form.cleaned_data.get("preco_max")
        quilometragem_max = form.cleaned_data.get("quilometragem_max")

        if nome:
            veiculos = veiculos.filter(
                nome__icontains=nome
            )  # se for preenchido, busca os veículos com o nome ou parte desse nome (incontain)

        if ano_min:
            veiculos = veiculos.filter(ano_modelo__gte=ano_min)

        if preco_max:
            veiculos = veiculos.filter(preco__lte=preco_max)

        if quilometragem_max:
            veiculos = veiculos.filter(quilometragem__lte=quilometragem_max)

    veiculos = veiculos.order_by("-ano_modelo", "preco")

    paginator = Paginator(veiculos, 8)
    page_number = request.GET.get(
        "page"
    )  # obtem o número da página atual a partir de "page" na url
    page_obj = paginator.get_page(page_number)  # mostra o objeto de acordo com a página

    return render(request, "painel.html", {"veiculos": page_obj, "form_filtro": form})


@login_required
def deletar_conta(request):
    if request.method == "POST":
        user = request.user
        username = user.username
        user.delete()  # deleta a conta do usuário
        messages.success(request, f"Conta {username} foi deletada com sucesso!")
        return redirect("home")

    return render(
        request, "deletar_conta.html"
    )  # se for um método GET, renderiza o template de confirmar a deletação da conta
