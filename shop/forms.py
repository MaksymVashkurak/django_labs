from django import forms

from .models import NewsletterSubscription, Rating


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
