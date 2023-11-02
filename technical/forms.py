from django import forms
from .models import Tsourcing

class TsourcingForm(forms.ModelForm):
    class Meta:
        model = Tsourcing
        fields = '__all__'
