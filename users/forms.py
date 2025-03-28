from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter password',
            'class': 'form-control',
            'required': True,
        })
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat password',
            'class': 'form-control',
            'required': True,
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Type a username',
                'class': 'form-control',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter email (eg. username@mail.com)',
                'class': 'form-control',
                'required': True,
            }),
        }


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Update email address',
        'class': 'form-control',
        'required': True,
    }))

    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Update username',
                'class': 'form-control',
                'required': True,
            }),
        }
