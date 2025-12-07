from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
)
from django.core.exceptions import (
    ValidationError,
)  # validação personalizada
from django.db.models.signals import pre_delete
from django.dispatch import receiver


# define os atributos de cada modelo, essencial no CRUD


class TipoUsuario(models.Model):
    nome_tipo = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.nome_tipo  # representar o objeto como uma string


class Cliente(
    AbstractUser
):  # define o modelo de usuário personalizado herdando campos padrão do Django
    cpf = models.CharField(max_length=11, unique=True, verbose_name="CPF")
    rua = models.CharField(max_length=255, blank=True, null=True)
    nome_cidade = models.CharField(max_length=100, blank=True, null=True)
    nome_bairro = models.CharField(max_length=100, blank=True, null=True)
    saldo = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name="Saldo"
    )

    def __str__(self):
        return f"{self.username} - {self.cpf}"

    @property
    def is_gerente(self):
        return self.groups.filter(name="Gerente").exists()

    @property
    def is_vendedor(self):
        return self.groups.filter(name="Vendedor").exists()

    @property
    def is_cliente(self):
        return self.groups.filter(name="Cliente").exists()

    REQUIRED_FIELDS = [
        "cpf",
        "email",
        "rua",
        "nome_cidade",
        "nome_bairro",
        "first_name",
        "last_name",
    ]  # lista de campos obrigatórios ao criar um usuário (precisa pra n deixar o superuser vazio)


class Veiculo(models.Model):
    nome = models.CharField(max_length=255)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    ano_modelo = models.IntegerField()
    quilometragem = models.IntegerField()
    potencia = models.CharField(max_length=100)
    consumo = models.CharField(max_length=100)
    historico_dono = models.TextField(blank=True, null=True)
    marca = models.CharField(max_length=100)
    foto_url = models.TextField(blank=True, null=True)

    def __str__(self):  # define a representação em string do objeto
        return f"{self.nome} ({self.ano_modelo})"


class StatusCredito(models.Model):
    nome_status = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.nome_status


class Compra(models.Model):
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE
    )  # FK para deletar a compra se o cliente for deletado
    veiculo = models.ForeignKey(
        Veiculo, on_delete=models.CASCADE
    )  # fk para deletar o veículo se a compra for deletada
    status_credito = models.ForeignKey(StatusCredito, on_delete=models.CASCADE)

    def __str__(self):
        return f"Compra {self.id} - {self.cliente.username}"


class Financeiro(models.Model):
    valor_cofre = models.DecimalField(max_digits=15, decimal_places=2)


class AquisicaoVeiculo(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    valor_compra = models.DecimalField(max_digits=10, decimal_places=2)
    data_aquisicao = models.DateField()


class TransacaoFinanceira(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, null=True, blank=True)
    aquisicao = models.ForeignKey(
        AquisicaoVeiculo, on_delete=models.CASCADE, null=True, blank=True
    )
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_transacao = models.CharField(max_length=20)
    data_transacao = models.DateTimeField(auto_now_add=True)


@receiver(pre_delete, sender=Cliente)  # atua antes de deletar um cliente
def delete_veiculos_of_deleted_cliente(
    sender, instance, **kwargs
):  # função para deletar veículos comprados pelo cliente
    # pega ids dos veículos comprados pelo cliente que vai deletar a conta
    veiculo_ids = list(
        Compra.objects.filter(cliente=instance).values_list("veiculo_id", flat=True)
    )
    if veiculo_ids:
        # deleta todos os veículos que tenham o ID na lista de compras do cliente
        Veiculo.objects.filter(id__in=veiculo_ids).delete()
