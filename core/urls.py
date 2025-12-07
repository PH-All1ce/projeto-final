from django.contrib.auth import (
    views as auth_views,
)  # views padrão do sistema de autenticação do django (usada para redefinir senha)
from django.urls import path  # defini o mapeamento de urls
from . import views  # importa as views
from .forms import (
    DefinirNovaSenhaForm,
)  # form personalizado para o sistema de troca de senha

# define quais funções são executadas quando uma url é acessada

urlpatterns = [  # padrão: URL | função da view que vai ser executada | nome da URL (usada nos templates)
    # Verificação de usuário
    path("login/", views.login_view, name="login"),
    path("registrar/", views.registrar_cliente, name="registrar_cliente"),
    path("logout/", views.logout_view, name="logout"),
    # carros
    path("", views.carros_listar, name="home"),
    path("veiculo/<int:id>/", views.veiculos_infos, name="veiculos_infos"),
    path("veiculo/criar/", views.veiculo_criar, name="veiculo_criar"),
    path("veiculo/<int:id>/editar/", views.veiculo_editar, name="veiculo_editar"),
    path("veiculo/<int:id>/remover/", views.veiculo_remover, name="vei-rm"),
    # Contas
    path("painel/", views.painel_vendedor, name="painel"),
    path("perfil/", views.meu_perfil, name="meu_perfil"),
    path("perfil/editar/", views.editar_perfil, name="editar_perfil"),
    path("deletar-conta/", views.deletar_conta, name="deletar_conta"),
    path(  # essas últimas são urls genéricas para o sistema de redefinir senha
        "password-reset/",
        auth_views.PasswordResetView.as_view(  # etapa de solicitação da troca de senha
            template_name="registration/password_reset_form.html",  # define os templates que devem ser usados (personalizados)
            email_template_name="registration/password_reset_email.html",
            success_url="/password-reset/done/",
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",  # informa que o e-mail foi enviado
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"  # define o template personalizado
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(  # exibe o template personalizado para redefinir a nova senha (com o form personalizado)
            template_name="registration/password_reset_confirm.html",
            form_class=DefinirNovaSenhaForm,
            success_url="/password-reset/complete/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete/",  # rota de confirmação de que a senha foi alterada com sucesso
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
