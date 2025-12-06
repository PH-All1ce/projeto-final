from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .forms import DefinirNovaSenhaForm

urlpatterns = [
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
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html",
            email_template_name="registration/password_reset_email.html",
            success_url="/password-reset/done/",
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            form_class=DefinirNovaSenhaForm,
            success_url="/password-reset/complete/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
