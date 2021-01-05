from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate



class LoginForm(forms.Form):
    username_login = forms.CharField(label='', min_length=4, max_length=150,
                                     widget=forms.TextInput(attrs={'placeholder': 'username'}))
    password_login = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'create a password'}))

    def clean(self):
        username = self.cleaned_data['username_login']
        password = self.cleaned_data['password_login']
        user = authenticate(username=username, password=password)

        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data['username_login']
        password = self.cleaned_data['password_login']
        user = authenticate(username=username, password=password)
        return user


choices = [
    ('Nursery', 'Nurser'),
    ('User', 'User'),
]


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required', widget=forms.TextInput(attrs={'autocomplete': 'off', 'placeholder': 'Email'}))
    username = forms.CharField(max_length=200, help_text='Required', widget=forms.TextInput(attrs={'autocomplete': 'off', 'placeholder': 'Username'}))
    password1 = forms.CharField(max_length=200, help_text='Required', widget=forms.PasswordInput(attrs={'autocomplete': 'off', 'placeholder': 'Password', 'data-toggle': 'password', 'id': 'pass1'}))
    password2 = forms.CharField(max_length=200, help_text='Required',
                                widget=forms.PasswordInput(attrs={'autocomplete': 'off', 'placeholder': 'Confirm Password', 'data-toggle': 'password', 'id': 'pass2'}))
    type = forms.ChoiceField(choices=choices)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2','type')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email

