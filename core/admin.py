from django.contrib import admin
from django.utils.html import format_html
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

@admin.register(TipoUsuario)
class TipoUsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome_tipo',)
    fields = ('nome_tipo',)
    


@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'marca', 'ano_modelo', 'preco', 'quilometragem', 'potencia', 'consumo', 'historico_dono', 'foto_preview')
    fields = ('nome', 'marca', 'ano_modelo', 'preco', 'quilometragem', 'potencia', 'consumo', 'historico_dono', 'foto_url')

    def foto_preview(self, obj):
        if obj.foto_url:
            return format_html('<img src="{}" style="width: 100px; height:auto;" />', obj.foto_url)
        return "No Image"
    foto_preview.short_description = 'Foto'

@admin.register(StatusCredito)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('nome_status',)
    fields = ('nome_status',)

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'veiculo', 'status_credito')
    fields = ('cliente', 'veiculo', 'status_credito')

@admin.register(Financeiro)
class FinanceiroAdmin(admin.ModelAdmin):
    list_display = ('valor_cofre',)
    fields = ('valor_cofre',)

@admin.register(AquisicaoVeiculo)
class AquisicaoAdmin(admin.ModelAdmin):
    list_display = ('veiculo', 'valor_compra', 'data_aquisicao')
    fields = ('veiculo', 'valor_compra', 'data_aquisicao')

@admin.register(TransacaoFinanceira)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ('compra', 'aquisicao', 'valor', 'tipo_transacao', 'data_transacao')
    fields = ('compra', 'aquisicao', 'valor', 'tipo_transacao')

