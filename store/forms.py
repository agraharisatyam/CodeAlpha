from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")


class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=200)
    email = forms.EmailField()
    address = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))

