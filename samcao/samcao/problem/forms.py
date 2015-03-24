from django import forms

class OldEmailBox(forms.Form):
    imapserver = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField()