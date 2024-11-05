"""Django user-forms"""
#Django
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class InternetUserCreationForm(UserCreationForm):
    
    username = forms.CharField(label=False,widget=forms.TextInput(attrs={"placeholder":"Username"}),required=True)
    
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Email"}),label=False,required=True)
    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"autocomplete": "new-password","placeholder":"Password"}),label=False,required=True)
    
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={"autocomplete": "new-password","placeholder":"Password confirmation"}),label=False,required=True)
    
    
    class Meta:
        model = User
        fields = ["username","email","password1","password2"]
        help_texts = {k:"" for k in fields}