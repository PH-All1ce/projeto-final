from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Veiculo, Cliente


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Nome de Usuário",
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label="Senha", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


class RegistroClienteForm(UserCreationForm):
    email = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"class": "form-control"})
    )
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
    endereco = forms.CharField(
        label="Endereço",
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
    tipo_usuario = forms.ChoiceField(
        choices=[("Cliente", "Cliente"), ("Vendedor", "Vendedor")],
        label="Tipo de Usuário",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Cliente
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "cpf",
            "endereco",
            "nome_cidade",
            "nome_bairro",
            "password1",
            "password2",
            "tipo_usuario",
        )
        labels = {
            "username": "Nome de Usuário",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["password1"].label = "Senha"
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password1"].help_text = (
            "Mínimo 8 caracteres, com letras e números."
        )

        self.fields["password2"].label = "Confirmar Senha"
        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["password2"].help_text = "Digite a mesma senha novamente."

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise forms.ValidationError("A senha deve ter no mínimo 8 caracteres.")
        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError("A senha deve conter pelo menos um número.")
        if not any(char.isalpha() for char in password1):
            raise forms.ValidationError("A senha deve conter pelo menos uma letra.")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não correspondem.")
        return password2

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf")
        if len(cpf) != 11:
            raise forms.ValidationError("CPF deve conter 11 dígitos.")
        if not cpf.isdigit():
            raise forms.ValidationError("CPF deve conter apenas números.")
        return cpf


class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = (
            "nome",
            "marca",
            "preco",
            "ano_modelo",
            "quilometragem",
            "potencia",
            "consumo",
            "historico_dono",
            "foto_url",
        )
        labels = {
            "nome": "Nome do Veículo",
            "marca": "Marca",
            "preco": "Preço",
            "ano_modelo": "Ano do Modelo",
            "quilometragem": "Quilometragem (KM)",
            "potencia": "Potência",
            "consumo": "Consumo (KM/L)",
            "historico_dono": "Histórico do Dono",
            "foto_url": "URL da Foto",
        }
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "marca": forms.TextInput(attrs={"class": "form-control"}),
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


class SaldoForm(forms.Form):
    saldo = forms.DecimalField(
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
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ex: 10000.00",
                "step": "0.01",
            }
        ),
    )


class VeiculoFiltroForm(forms.Form):
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
            attrs={"class": "form-control", "placeholder": "Ex: 50000", "step": "1000"}
        ),
    )
    quilometragem_max = forms.IntegerField(
        label="Quilometragem Máxima (KM)",
        required=False,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Ex: 100000"}
        ),
    )
