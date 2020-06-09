from django import forms
from .models import *


class NewsletterUserSignUpForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'input-element newsletter',
        'placeholder': 'Email'
    }))
    class Meta:
        model = NewsletterUser
        fields = ['email']
        
        def clean_email(self):
            email = self.cleaned_data.get('email')
            
            return email

