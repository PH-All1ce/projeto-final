from django.contrib import admin
from django.urls import path, include
from core import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.carros_listar, name="home"),
    path('veiculo_infos/<int:id>/', views.veiculos_infos, name='veiculo_info'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('painel/', views.painel_vendedor, name='painel'),
    path('painel/veiculo_criar/', views.veiculo_criar, name='veiculo_criar'),
    path('painel/veiculo_editar/<int:id>/', views.veiculo_editar, name='veiculo_editar'),
    path('painel/veiculo_remover/<int:id>/', views.veiculo_remover, name='vei-rm'),
    path('accounts/', include('django.contrib.auth.urls')),
]