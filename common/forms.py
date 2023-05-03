from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from .models import User
from rest_framework.validators import UniqueValidator

class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일",required=True)

    class Meta:
        model = User
        # model.username.unique = True
        # model.email.unique=True
        fields = ("username", "password1", "password2", "email")
