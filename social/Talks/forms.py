from django import forms
from .models import Talks


class TalkForm(forms.ModelForm):
    body = forms.CharField(required=True,
                           widget=forms.widgets.Textarea(
                               attrs={
                                   "placeholder": "Share Your Thoughts",
                                   "class": "form-control",
                               }
                           ),
                           label="",
                           )

    class Meta:
        model = Talks
        exclude = ("user",)
