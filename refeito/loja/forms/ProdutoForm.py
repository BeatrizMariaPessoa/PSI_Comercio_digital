from django.forms import ModelForm
from django import forms

from loja.models.Produto import Produto

class ProdutoCreateForm(ModelForm):
    class Meta:
        fields = ['Produto', 'destaque', 'promocao', 'msgPromocao', 'preco', 'categoria', 'fabricante', 'image']
        model = Produto
        widgets = {
            'Produto': forms.TextInput(attrs={'class': "form-control"}),
            'destaque': forms.CheckboxInput(attrs={'class': "form-check-input"}),
            'promocao': forms.CheckboxInput(attrs={'class': "form-check-input"}),
            'msgPromocao': forms.TextInput(attrs={'class': "form-control"}),
            'preco': forms.NumberInput(attrs={'class': "form-control"}), #Pode dar problema
            'categoria': forms.Select(attrs={'class': "form-control"}),
            'fabricante': forms.Select(attrs={'class': "form-control"}),
            'image': forms.FileInput(attrs={'class': "form-control"})
        }