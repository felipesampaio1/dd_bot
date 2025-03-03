from django import forms

from taxpayers.models import Payer


class PayerForm(forms.ModelForm):
    class Meta:
        model = Payer
        fields = ['cpf', 'payer_name', 'partner', 'phone', 'initial_requirement', 'inss_requirement', 'doctor', 'social', 'daily_update', 'der']
        labels = {
            'cpf': 'CPF',
            'payer_name': 'Nome do Pagador',
            'partner': 'Parceiro',
            'phone': 'Telefone',
            'initial_requirement': 'Requerimento Inicial',
            'inss_requirement': 'Requerimento INSS',
            'doctor': 'Avaliação Médica',
            'social': 'Avaliação Social',
            'daily_update': 'Atualização Diária',
            'der': 'DER',
        }
    widgets = {
        'doctor': forms.CheckboxInput(attrs={'class': 'filled-in'}),
        'social': forms.CheckboxInput(attrs={'class': 'filled-in'}),
    }
