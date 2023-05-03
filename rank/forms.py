from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from .models import Order
from rest_framework.validators import UniqueValidator

class OrderForm(forms.Form):
    target_time = forms.CharField(label="타겟시간",required=True)
    keyword = forms.CharField(label="키워드", required=True)
    target_url = forms.CharField(label="주소", required=True)
    charge = forms.IntegerField( required=True)


    class Meta:
        model = Order

        fields = ("order_time", "keyword", "target_url", "charge")
