from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)  # renderizar templates | redirecionar para URLs | buscar objetos ou erro
from django.contrib.auth import (
    authenticate,
    login,
    logout,
)  # verificar credencial | iniciar e encerrar sessão
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
)  # restringe o acesso as views para logados/ com permissão
from django.contrib import (
    messages,
)  # framework de mensagem (sucesso ou erro para o usuário)
from django.contrib.auth.models import Group  # gerenciar grupos de usuários
from .models import Veiculo, Compra, StatusCredito  # importa modelos
from .forms import (
    VeiculoForm,
    LoginForm,
    RegistroClienteForm,
    VeiculoFiltroForm,
    SaldoForm,
    PerfilEditForm,
)  # importa formulários
from django.contrib.auth import logout
from django.core.paginator import Paginator  # paginação

# recebe as requisições, define a lógica da resposta e devolve as respostas adequadas

# LOGIN LOGOUT REGISTRO EDITAR PERFIL


@login_required  # verifica se está logado
def meu_perfil(request):
    user = request.user
    saldo_form = SaldoForm()  # formulário para atualizar saldo
    comprados = Compra.objects.filter(cliente=user).select_related(
        "veiculo"
    )  # veículos comprados pelo usuário

    if request.method == "POST":
        saldo_form = SaldoForm(
            request.POST
        )  # post "postar" dados, dados não são enviadas pelo url, mas pelo corpo da requisição
        if saldo_form.is_valid():  # se for válido o valor será atualizado
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
    )  # renderiazar o template com os dados do usuário


def login_view(request):  # serve para autenticar o usuário de acordo com o loginform
    login_error = None
    if request.method == "POST":  # envia os dados
        form = LoginForm(request.POST)  # carrega o formulário com os dados enviados
        if form.is_valid():  # verifica se os dados abaixo são válidos
            username = form.cleaned_data["username"]
            senha = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=senha)
            if user:  # se for validado, loga e aparece mensagem de sucesso
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
):  # encerra a sessão do usuário e redireciona para o menu principal
    logout(request)
    return redirect("home")


def registrar_cliente(request):
    if request.method == "POST":  # post para enviar os dados
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            grupo, created = Group.objects.get_or_create(
                name="Cliente"
            )  # usuário é adicionado ao grupo cliente
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


@login_required  # verifica se está logado
def editar_perfil(request):
    user = request.user
    if (
        request.method == "POST"
    ):  # se o POST for válido, salva as alterações e redireciona para o perfil
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
    )  # busca todos os veículos
    veiculos = Veiculo.objects.exclude(
        id__in=veiculos_comprados
    )  # exclui os veículos que já foram comprados e mostra só os disponíveis
    form = VeiculoFiltroForm(request.GET)  # instancia do form de filtro

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
            )  # se for preenchido, busca os veículos com o nome ou parte desse nome.

        if ano_min:
            veiculos = veiculos.filter(
                ano_modelo__gte=ano_min
            )  # mostra os veículos com o ano igual ou maior

        if preco_max:
            veiculos = veiculos.filter(
                preco__lte=preco_max
            )  # mostra os veículos com o preço igual o menor

        if quilometragem_max:
            veiculos = veiculos.filter(
                quilometragem__lte=quilometragem_max
            )  # mostra veículos com a quilometragem igual ou menor

    veiculos = veiculos.order_by(
        "-ano_modelo", "preco"
    )  # ordena a listagem de acordo com o ano (mais novo) e o preço (mais barato)

    paginator = Paginator(veiculos, 8)  # 8 veículos por página
    page_number = request.GET.get(
        "page"
    )  # obtem o número da página atual a partir de "page" na url
    page_obj = paginator.get_page(page_number)  # mostra o objeto de acordo com a página

    return render(
        request, "home.html", {"veiculos": page_obj, "form_filtro": form}
    )  # renderiza o home com os veículos de cada página e o filtro


@login_required  # exige que esteja logado
@permission_required(
    "core.add_veiculo", login_url="/login/"
)  # requere permissão (do django admin), se não tiver vai para o login
def veiculo_criar(request):
    if (
        request.method == "POST"
    ):  # se POST, verifica se o forms de veic foi preenchido corretamente e da a mensagem de sucesso ou erro
        form = VeiculoForm(
            request.POST, request.FILES
        )  # instancia form e preenche com os dados informados
        if form.is_valid():
            form.save()  # salva o novo veic no banco de dados
            messages.success(request, "Veículo criado com sucesso!")
            return redirect("painel")  # redireciona para a url do painel
        else:
            messages.error(request, "Erro ao criar veículo. Verifique os campos.")
    else:  # se GET, motra o formulário vazio, para criar o veículo
        form = VeiculoForm()  # instancia do formulário vazio
    return render(
        request, "formveiculo.html", {"form": form}
    )  # renderiza o template vazio e passa a instancia vazia do form


@login_required  # exige que esteja logado
@permission_required(
    "core.change_veiculo", login_url="/login/"
)  # exige permissão de editar o veículo, se não tiver manda para o login
def veiculo_editar(request, id):  # além do request recebe o id
    veiculo = get_object_or_404(Veiculo, id=id)  # procura o veículo ou retorna um erro
    if request.method == "POST":
        form = VeiculoForm(
            request.POST, request.FILES, instance=veiculo
        )  # se for POST, a instancia do veículo será carregada para ser atualizada
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
    return render(
        request, "formveiculo.html", {"form": form}
    )  # renderiza o template do formulário de edição


@login_required  # exige login
@permission_required(
    "core.delete_veiculo", login_url="/login/"
)  # só pode ser utilizado se tiver permissão de deletar (do admin), ou vai para login
def veiculo_remover(request, id):  # recebe a requisição + id
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


@login_required  # exige login
def veiculos_infos(request, id):  # recebe a requisição + id
    veiculo = get_object_or_404(Veiculo, id=id)  # busca o objeto ou retorna o erro

    if request.method == "POST":
        if (
            request.user.saldo >= veiculo.preco
        ):  # verifica se da para comprar o veic com o saldo
            request.user.saldo -= veiculo.preco  # subtrai o preço do veic do saldo
            request.user.save()  # atualiza o novo saldo

            status_aprovado, created = StatusCredito.objects.get_or_create(
                nome_status="Aprovado"
            )
            Compra.objects.create(  # cria um novo registro na tabela de compra, ligando o cliente ao veic (indicando como aprovado)
                cliente=request.user, veiculo=veiculo, status_credito=status_aprovado
            )

            messages.success(  # mensagem de sucesso com o saldo atualizado
                request,
                f"Veículo {veiculo.nome} comprado com sucesso! Saldo restante: R$ {request.user.saldo:.2f}",
            )
            return redirect("home")  # redireciona para home
        else:  # se o saldo for insuficiente, manda um erro
            messages.error(request, "Saldo insuficiente para comprar este veículo.")
    # se for um GET ou der erro de saldo, apenas mostra a informação do veículo
    return render(request, "infos.html", {"veiculo": veiculo})


@login_required  # exige login
@permission_required(
    "core.change_veiculo", login_url="/login/"
)  # exige permissão do admin do django
def painel_vendedor(request):
    veiculos_comprados = Compra.objects.values_list(
        "veiculo_id", flat=True
    )  # busca todos os veículos
    veiculos = Veiculo.objects.exclude(id__in=veiculos_comprados).order_by(
        "-ano_modelo", "preco"
    )  # exclui os veículos que já foram comprados e mostra só os disponíveis, organizando por ano e preço
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
            )  # se for preenchido, busca os veículos com o nome ou parte desse nome.

        if ano_min:
            veiculos = veiculos.filter(
                ano_modelo__gte=ano_min
            )  # mostra os veículos com o ano igual ou maior

        if preco_max:
            veiculos = veiculos.filter(
                preco__lte=preco_max
            )  # mostra veículos com a quilometragem igual ou menor

        if quilometragem_max:
            veiculos = veiculos.filter(
                quilometragem__lte=quilometragem_max
            )  # mostra veículos com a quilometragem igual ou menor

    veiculos = veiculos.order_by(
        "-ano_modelo", "preco"
    )  # ordena a listagem de acordo com o ano (mais novo) e o preço (mais barato)

    paginator = Paginator(veiculos, 8)  # 8 veículos por página
    page_number = request.GET.get(
        "page"
    )  # obtem o número da página atual a partir de "page" na url
    page_obj = paginator.get_page(page_number)  # mostra o objeto de acordo com a página

    return render(
        request, "painel.html", {"veiculos": page_obj, "form_filtro": form}
    )  # renderiza o home com os veículos de cada página e o filtro


@login_required  # exige login
def deletar_conta(request):
    if request.method == "POST":  # se a requisição for POST,
        user = request.user  # obtem o usuário logado
        username = (
            user.username
        )  # salva o nome de usuário (apenas para a mensagem de sucesso)
        user.delete()  # deleta a conta do usuário
        messages.success(
            request, f"Conta {username} foi deletada com sucesso!"
        )  # mensagem de sucesso
        return redirect("home")  # redireciona para home

    return render(
        request, "deletar_conta.html"
    )  # se for um método GET, renderiza o template de confirmar a deletação da conta
