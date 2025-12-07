from django.db import models  # biblioteca base do django para os models
from django.contrib.auth.models import (
    AbstractUser,
)  # biblioteca para customizar o user model
from django.core.exceptions import (
    ValidationError,
)  # biblioteca para validações personalizadas
from django.db.models.signals import pre_delete  # biblioteca para sinais do django
from django.dispatch import receiver  # biblioteca para receber sinais do django


# define os atributos de cada modelo, essencial no CRUD


class TipoUsuario(models.Model):
    nome_tipo = models.CharField(max_length=20, unique=True)

    def __str__(self):  # define a representação em string do objeto
        return self.nome_tipo  # representar o objeto como uma string


class Cliente(
    AbstractUser
):  # define o modelo de usuário personalizado herdando campos padrão do Django
    cpf = models.CharField(
        max_length=11, unique=True, verbose_name="CPF"
    )  # único, máximo de 11 caracteres
    rua = models.CharField(max_length=255, blank=True, null=True)
    nome_cidade = models.CharField(max_length=100, blank=True, null=True)
    nome_bairro = models.CharField(max_length=100, blank=True, null=True)
    saldo = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name="Saldo"
    )  # saldo do cliente

    def __str__(self):
        return f"{self.username} - {self.cpf}"  # retorna o nome de usuário e CPF do cliente

    @property
    def is_gerente(self):
        return self.groups.filter(
            name="Gerente"
        ).exists()  # verifica se o usuário é um gerente e retorna True se for

    @property
    def is_vendedor(self):
        return self.groups.filter(
            name="Vendedor"
        ).exists()  # verifica se o usuário é um vendedor e retorna True se for

    @property
    def is_cliente(self):
        return self.groups.filter(
            name="Cliente"
        ).exists()  # verifica se o usuário é um cliente e retorna True se for

    REQUIRED_FIELDS = [
        "cpf",
        "email",
        "rua",
        "nome_cidade",
        "nome_bairro",
        "first_name",
        "last_name",
    ]  # lista de campos obrigatórios ao criar um usuário (essencial para o superuser não ficar vazio)


class Veiculo(models.Model):  # define o modelo de veículo
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
        return f"{self.nome} ({self.ano_modelo})"  # retorna o nome e o ano do modelo do veículo


class StatusCredito(models.Model):  # define o modelo de status de crédito
    nome_status = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.nome_status


class Compra(models.Model):  # modelo do registro de compra
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE
    )  # FK para deletar a conta se o cliente for deletado
    veiculo = models.ForeignKey(
        Veiculo, on_delete=models.CASCADE
    )  # fk para deletar o veículo se a compra for deletada
    status_credito = models.ForeignKey(
        StatusCredito, on_delete=models.CASCADE
    )  # fk para o status do crédito

    def __str__(self):  # representação do objeto como string
        return f"Compra {self.id} - {self.cliente.username}"


class Financeiro(models.Model):  # valor total no cofre da empresa
    valor_cofre = models.DecimalField(max_digits=15, decimal_places=2)


class AquisicaoVeiculo(models.Model):  # registro de aquisição de veículos
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    valor_compra = models.DecimalField(max_digits=10, decimal_places=2)
    data_aquisicao = models.DateField()


class TransacaoFinanceira(models.Model):  # registrar entradas e saídas financeiras
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
        # deleta todos os veículos da tabela veículo que tenham o ID na lista de compras do cliente
        Veiculo.objects.filter(id__in=veiculo_ids).delete()
