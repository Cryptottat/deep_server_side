from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

class CreatePaymentForm(forms.Form):
    order_point = forms.IntegerField( required=True)
    class Meta:
        fields = ("order_point")
