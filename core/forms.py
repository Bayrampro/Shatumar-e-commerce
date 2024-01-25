from captcha.fields import CaptchaField
from django import forms
from django.utils.translation import gettext_lazy as _
from core.models import Feedback


class FeedbackForm(forms.ModelForm):
    user = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    subject = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': 7, 'cols': 30}))
    captcha = CaptchaField()

    class Meta:
        model = Feedback
        fields = ['user', 'email', 'subject']