from django import forms

class OldEmailBox(forms.Form):
    imapserver = forms.CharField(min_length=5,label='OldEmailServer')
    email = forms.EmailField(min_length=5,label='EmailAddress')
    password = forms.CharField(min_length=5,label='PassWord')