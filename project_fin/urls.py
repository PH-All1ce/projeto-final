from django.contrib import admin
from django.urls import path, include
from core.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", carros_listar, name="home"),
    path('painel/', painel_vendedor, name='painel'),
    path('painel/veiculo_remover/<int:id>/', veiculo_remover, name='vei-rm'),
    path('painel/veiculo_criar/', veiculo_criar, name='veiculo_criar'),
    path('painel/veiculo_editar/<int:id>/', veiculo_editar, name='veiculo_editar'),
    path('registrar/', registrar_cliente, name='registrar'),
    path('veiculo/<int:id>/', veiculos_infos, name='veiculos_infos'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('meu-perfil/', meu_perfil, name='meu_perfil'),
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'core' / 'static')