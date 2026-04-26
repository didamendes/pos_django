from django import forms
from .models import pessoa


class PessoaForm(forms.ModelForm):
    class Meta:
        model = pessoa
        fields = ['nome', 'email', 'fone', 'funcao', 'nascimento', 'ativo']
        widgets = {
            'nascimento': forms.DateInput(attrs={'type': 'date'}),
        }
