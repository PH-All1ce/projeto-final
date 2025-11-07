from django.forms import ModelForm
from django import forms
from .models import Veiculo, Cliente
from django.contrib.auth.forms import UserCreationForm

class VeiculoForm(ModelForm):

    class Meta:
        model = Veiculo
        fields = '__all__'
        widgets = {
            'nome' : forms.TextInput(attrs={'class': 'form-control' }),
            'preco' : forms.NumberInput(attrs={'class': 'form-control' }),
            'ano_modelo' : forms.NumberInput(attrs={'class': 'form-control' }),
            'quilometragem': forms.NumberInput(attrs={'class': 'form-control' }),
            'potencia': forms.TextInput(attrs={'class': 'form-control' }),
            'consumo': forms.TextInput(attrs={'class': 'form-control' }),
            'historico_dono': forms.Textarea(attrs={'class': 'form-control' }),
            'marca': forms.TextInput(attrs={'class': 'form-control' }),
            'foto_url': forms.URLInput(attrs={'class': 'form-control'}),
        }

class ClienteForm(ModelForm):

    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'tipo_usuario' : forms.Select(attrs={'class': 'form-control' }),
            'nome' : forms.TextInput(attrs={'class': 'form-control' }),
            'cpf' : forms.TextInput(attrs={'class': 'form-control' }),
            'email' : forms.EmailInput(attrs={'class': 'form-control' }),
            'senha' : forms.PasswordInput(attrs={'class': 'form-control' }),
            'endereco_entrega': forms.TextInput(attrs={'class': 'form-control' }),
        }

class RegistroClienteForm(UserCreationForm):
    TIPO_USUARIO_CHOICES = [
        ('Cliente', 'Cliente'),
        ('Vendedor', 'Vendedor'),
        ('Gerente', 'Gerente'),
    ]
    tipo_usuario = forms.ChoiceField(choices=TIPO_USUARIO_CHOICES, label="Tipo de conta")

    class Meta:
        model = Cliente
        fields = ['username', 'email', 'cpf', 'endereco', 'nome_cidade', 'nome_bairro', 'password1', 'password2', 'tipo_usuario']
        
class LoginForm(forms.Form):
    username = forms.CharField(label="Usuário")
    password = forms.CharField(widget=forms.PasswordInput)
