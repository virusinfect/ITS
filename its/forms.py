# forms.py
from django import forms
from .models import Comment,Remark

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.TextInput(attrs={'class': 'form-control'}),
        }

class RemarkForm(forms.ModelForm):
    class Meta:
        model = Remark
        fields = ['remark']
        widgets = {
            'remark': forms.TextInput(attrs={'class': 'form-control'}),
        }

class RowForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    file = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))
class EmailForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))