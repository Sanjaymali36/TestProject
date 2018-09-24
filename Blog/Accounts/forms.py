from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
class UserRegistrationForm(forms.Form):
    username = forms.CharField(label='User Name',
                                                min_length=3,
                                                max_length=100,
                                                widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Password',min_length=8,
                                                max_length=100,
                                                widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password',min_length=8,
                                                max_length=100,
                                                widget=forms.PasswordInput(attrs={'class':'form-control'}))


    def clean_email(self):
        email = self.cleaned_data['email']
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise ValidationError('Email Id is already exists!')
        return email

    def clean_password2(self):
        p2 = self.cleaned_data['password2']
        p1 = self.cleaned_data['password1']
        if p2 and p1:
            if p2 != p1:
                raise ValidationError('Password Not Matched!')
        return p2
