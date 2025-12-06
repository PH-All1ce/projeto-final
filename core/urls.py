from django.urls import path
from . import views

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
]
