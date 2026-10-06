from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'customer_id', 'name', 'email', 'tenure', 
            'balance', 'transaction_frequency', 'complaints', 'service_usage'
        ]
        widgets = {
            'customer_id': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'tenure': forms.NumberInput(attrs={'class': 'form-control'}),
            'balance': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'transaction_frequency': forms.NumberInput(attrs={'class': 'form-control'}),
            'complaints': forms.NumberInput(attrs={'class': 'form-control'}),
            'service_usage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

