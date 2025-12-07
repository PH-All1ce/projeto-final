from django import forms  # modulo base de formulários django
from django.contrib.auth.models import (
    User,
)  # biblioteca para o modelo de usuário padrão do django
from django.contrib.auth.forms import (
    UserCreationForm,
)  # formulário base para criação de usuários (possuilógica de senha)
from .models import Veiculo, Cliente  # importa os models
from django.contrib.auth.forms import (
    SetPasswordForm,
)  # formulário base para redefinir senha (não precisa da antiga)

# interage com o models e cria e valida formulários html


class LoginForm(forms.Form):  # formulário simples sem ligação com model
    username = forms.CharField(
        label="Nome de Usuário",
        max_length=150,
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),  # form-control é classe do bootstrap para estilização
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(
            attrs={"class": "form-control"}
        ),  # deixar a senha oculta enquanto digita
    )  # form-control para estilizar


class RegistroClienteForm(
    UserCreationForm
):  # registrar; extende o formulário de criação de usuário do django
    email = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"class": "form-control"})
    )  # definição dos campos de usuário com os atributos
    first_name = forms.CharField(
        label="Primeiro Nome",
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    last_name = forms.CharField(
        label="Último Nome",
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    cpf = forms.CharField(
        label="CPF",
        max_length=11,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "00000000000"}
        ),
    )
    rua = forms.CharField(
        label="Rua",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    nome_cidade = forms.CharField(
        label="Cidade",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    nome_bairro = forms.CharField(
        label="Bairro",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    class Meta:  # classe interna para definir o modelo e campos do formulário
        model = Cliente  # modelo cliente que está associado ao form
        fields = (  # lista de campos do cliente
            "username",
            "email",
            "first_name",
            "last_name",
            "cpf",
            "rua",
            "nome_cidade",
            "nome_bairro",
            "password1",
            "password2",
        )
        labels = {  # rótulo personalizado
            "username": "Nome de Usuário",
        }

    def __init__(
        self, *args, **kwargs
    ):  # inicializa o formulário e personaliza os campos
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["password1"].label = (
            "Senha"  # personalização do campo senha e dos erros
        )
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password1"].help_text = (
            "Mínimo 8 caracteres, com letras e números."
        )

        self.fields["password2"].label = "Confirmar Senha"
        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["password2"].help_text = "Digite a mesma senha novamente."

    def clean_password1(
        self,
    ):  # validação personalizada (mínimo de caracteres e letras/números)
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise forms.ValidationError("A senha deve ter no mínimo 8 caracteres.")
        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError("A senha deve conter pelo menos um número.")
        if not any(char.isalpha() for char in password1):
            raise forms.ValidationError("A senha deve conter pelo menos uma letra.")
        return password1

    def clean_password2(self):  # verifica se a segunda senha é igual a primeira
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não correspondem.")
        return password2

    def clean_cpf(self):  # garante que o CPF tenha 11 dígitos e só números
        cpf = self.cleaned_data.get("cpf")
        if len(cpf) != 11:
            raise forms.ValidationError("CPF deve conter 11 dígitos.")
        if not cpf.isdigit():
            raise forms.ValidationError("CPF deve conter apenas números.")
        return cpf

    def save(self, commit=True):
        user = super().save(commit=False)

        user.tipo_usuario = "Cliente"  # define o tipo de usuário como cliente ao salvar (vendedores só podem ser promovidos pelo Superuser)
        if commit:
            user.save()
        return user


class PerfilEditForm(forms.ModelForm):  # editar perfil do cliente
    class Meta:
        model = Cliente  # modelo que vai ser editado
        fields = (  # lista dos campos editáveis (CPF não deve ser editável)
            "email",
            "rua",
            "nome_bairro",
            "nome_cidade",
            "first_name",
            "last_name",
        )
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "rua": forms.TextInput(
                attrs={"class": "form-control"}
            ),  # aplica o CSS nos campos
            "nome_bairro": forms.TextInput(attrs={"class": "form-control"}),
            "nome_cidade": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
        }


class VeiculoForm(forms.ModelForm):  # form para criar/editar veículos
    class Meta:
        model = Veiculo  # modelo veículo que será utilizado no criação/edição
        fields = (
            "nome",  # todos os campos do veículo de veículo utilizados na criação/edição
            "marca",
            "preco",
            "ano_modelo",
            "quilometragem",
            "potencia",
            "consumo",
            "historico_dono",
            "foto_url",
        )
        labels = {  # rótulos para os campos do formulário
            "nome": "Nome do Veículo",
            "marca": "Marca",
            "preco": "Preço",
            "ano_modelo": "Ano do Modelo",
            "quilometragem": "Quilometragem (KM)",
            "potencia": "Potência (HP)",
            "consumo": "Consumo (KM/L)",
            "historico_dono": "Histórico do antigo dono",
            "foto_url": "URL da Foto",
        }
        widgets = {
            "nome": forms.TextInput(
                attrs={"class": "form-control"}
            ),  # define o tipo de "texto" que é aceitado
            "marca": forms.TextInput(attrs={"class": "form-control"}),  # inclui O CSS
            "preco": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "ano_modelo": forms.NumberInput(attrs={"class": "form-control"}),
            "quilometragem": forms.NumberInput(attrs={"class": "form-control"}),
            "potencia": forms.TextInput(attrs={"class": "form-control"}),
            "consumo": forms.TextInput(attrs={"class": "form-control"}),
            "historico_dono": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
            "foto_url": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Cole a URL da imagem"}
            ),
        }


class SaldoForm(forms.Form):  # formulário simples para adicionar saldo ao cliente
    saldo = forms.DecimalField(  # campo decimal com validações
        label="Novo Saldo (R$)",
        max_digits=10,
        decimal_places=2,
        min_value=0,
        error_messages={
            "invalid": "Digite um número válido.",
            "max_digits": "Certifique-se de que não haja mais de %(max)s dígitos no total.",
            "max_decimal_places": "Certifique-se de que não haja mais de %(max)s casas decimais.",
            "max_whole_digits": "Certifique-se de que não haja mais de %(max)s dígitos antes da vírgula.",
            "min_value": "Certifique-se de que o valor seja maior ou igual a %(limit_value)s.",
        },
        widget=forms.NumberInput(  # entrada númerica, inclui css
            attrs={
                "class": "form-control",
                "placeholder": "Ex: 10000.00",
                "step": "0.01",
            }
        ),
    )


class VeiculoFiltroForm(
    forms.Form
):  # filtragem de veículos, todos os campos são opcionais
    nome = forms.CharField(
        label="Nome do Veículo",
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Ex: Corolla"}
        ),
    )
    ano_min = forms.IntegerField(
        label="Ano Mínimo",
        required=False,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Ex: 2020"}
        ),
    )
    preco_max = forms.DecimalField(
        label="Preço Máximo (R$)",
        required=False,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Ex: 50000", "step": "any"}
        ),
    )
    quilometragem_max = forms.IntegerField(
        label="Quilometragem Máxima (KM)",
        required=False,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Ex: 100000"}
        ),
    )


class DefinirNovaSenhaForm(
    SetPasswordForm
):  # redefinir senha, extende o formulário base do django
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # inicializa o form
        self.fields["new_password1"].label = "Nova Senha"
        self.fields["new_password1"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Digite a nova senha",
            }  # rótulo e placeholder (texto dentro do campo)
        )

        self.fields["new_password2"].label = "Confirmar Nova Senha"
        self.fields["new_password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Confirme a nova senha"}
        )
