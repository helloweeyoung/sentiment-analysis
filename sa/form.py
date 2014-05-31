from django.forms import ModelForm
from django import forms
from models import textfragment

class saForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'size':'75', 'class':'text_input'}))
    class Meta:
        model = textfragment
        fields = ['name']
# for django 1.2
#        widgets = {
#            'name': TextInput(attrs={'size': 200}),
#        }

