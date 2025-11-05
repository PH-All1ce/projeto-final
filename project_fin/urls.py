from django.contrib import admin
from django.urls import path
from core.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", carros_listar, name="home"),
    path('logout/', logout_view, name='logout'),
    path('painel/', painel_vendedor, name='painel'),
    path('painel/veiculo_remover/<int:id>/', veiculo_remover, name='vei-rm'),
    path('painel/veiculo_criar/', veiculo_criar, name='veiculo_criar'),
    path('painel/veiculo_editar/<int:id>/', veiculo_editar, name='veiculo_editar'),
    path('registrar/', registrar_cliente, name='registrar'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
