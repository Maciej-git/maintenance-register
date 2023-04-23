from django.forms import  ModelForm
from .models import Machine, Request, Note
from django import forms

class MachineForm(ModelForm):
    class Meta:
        model = Machine
        fields = ['manufacturer', 'type', 'sn', 'const_year', 'intern_symbol', 'intern_no', 'condition', 'location', 'group']
        widgets = {'manufacturer': forms.TextInput(attrs={'class': 'form-control'}),
                   'type': forms.TextInput(attrs={'class': 'form-control'}),
                   'sn': forms.TextInput(attrs={'class': 'form-control'}),
                   'const_year': forms.NumberInput(attrs={'class': 'form-control'}),
                   'intern_symbol':forms.TextInput(attrs={'class': 'form-control'}),
                   'intern_no': forms.NumberInput(attrs={'class': 'form-control'}),
                   'condition': forms.Select(attrs={'class': 'form-control'}),
                   'location': forms.Select(attrs={'class': 'form-control'}),
                   'group': forms.Select(attrs={'class': 'form-control'})
                   }
    
class selectMachine(ModelForm):
    class Meta:
        model = Machine
        fields = "__all__"
        widgets = {'manufacturer': forms.Select(attrs={'class': 'form-control'}),
                   'type': forms.TextInput(attrs={'class': 'form-control'}),
                   'sn': forms.TextInput(attrs={'class': 'form-control'}),
                   'const_year': forms.NumberInput(attrs={'class': 'form-control'}),
                   'intern_symbol':forms.Select(attrs={'class': 'form-control'}),
                   'intern_no': forms.NumberInput(attrs={'class': 'form-control'}),
                   'condition': forms.Select(attrs={'class': 'form-control'}),
                   'location': forms.Select(attrs={'class': 'form-control'}),
                   'group': forms.Select(attrs={'class': 'form-control'})
                   }
        
class newRequest(ModelForm):
    class Meta:
        model = Request
        fields = ['machine', 'issue']
        widgets = {'machine': forms.Select(attrs={'class': 'form-control'}),
                   'issue': forms.Textarea(attrs={'class': 'form-control'})}
        
class newNote(ModelForm):
    class Meta:
        model = Note
        fields = ['text']
        widgets = {'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'What is the reason of Hold?'})}