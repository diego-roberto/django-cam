from django import forms
from .models import Funcionario, Projeto

class FuncionarioForm(forms.ModelForm):
    cpf = forms.CharField(max_length=14, widget=forms.TextInput(attrs={'placeholder': '000.000.000-00', 'data-mask': '000.000.000-00'}))
    rg = forms.CharField(max_length=11, widget=forms.TextInput(attrs={'placeholder': '00.000.000-0', 'data-mask': '00.000.000-0'}))

    class Meta:
        model = Funcionario
        fields = '__all__'

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        cpf = cpf.replace('.', '').replace('-', '')
        if not cpf.isdigit():
            raise forms.ValidationError("CPF deve conter apenas números.")
        if len(cpf) != 11:
            raise forms.ValidationError("CPF deve conter 11 dígitos.")
        return cpf

    def clean_rg(self):
        rg = self.cleaned_data['rg']
        rg = rg.replace('.', '').replace('-', '')
        if not rg.isdigit():
            raise forms.ValidationError("RG deve conter apenas números.")
        return rg

class ProjetoAdminForm(forms.ModelForm):
    funcionarios = forms.ModelMultipleChoiceField(
        queryset=Funcionario.objects.all(),
        widget=forms.SelectMultiple,
    )

    class Meta:
        model = Projeto
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['supervisor'].queryset = Funcionario.objects.filter(is_supervisor=True)
