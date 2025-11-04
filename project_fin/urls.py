"""
URL configuration for project_fin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
    path('painel/veiculo_remover/', veiculos_listar_remover, name='vei-list-rm'),
    path('painel/veiculo_criar/', veiculo_criar, name='veiculo_criar'),
    path('painel/veiculo_editar/<int:id>/', veiculo_editar, name='veiculo_editar'),
    path('registrar/', registrar_cliente, name='registrar'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
