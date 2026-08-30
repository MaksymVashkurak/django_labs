from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import NewsletterSubscription, Order, Rating


class NewsletterSubscriptionForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = ["name", "email"]


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["name", "score", "comment"]
        widgets = {
            "score": forms.Select(choices=[(value, value) for value in range(1, 6)]),
            "comment": forms.Textarea(attrs={"rows": 3}),
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["customer_name", "email", "phone", "address"]


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField()


class PasswordResetConfirmForm(forms.Form):
    email = forms.EmailField()
    code = forms.CharField(max_length=6)
    new_password = forms.CharField(widget=forms.PasswordInput)
