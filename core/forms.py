from django.forms import ModelForm
from django import forms
from .models import Veiculo, Usuario

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

class UsuarioForm(ModelForm):

    class Meta:
        model = Usuario
        fields = '__all__'
        widgets = {
            'tipo_usuario' : forms.Select(attrs={'class': 'form-control' }),
            'nome' : forms.TextInput(attrs={'class': 'form-control' }),
            'cpf' : forms.TextInput(attrs={'class': 'form-control' }),
            'email' : forms.EmailInput(attrs={'class': 'form-control' }),
            'senha' : forms.PasswordInput(attrs={'class': 'form-control' }),
            'endereco_entrega': forms.TextInput(attrs={'class': 'form-control' }),
        }

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)