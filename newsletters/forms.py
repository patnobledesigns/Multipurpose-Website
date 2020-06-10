from django import forms
from .models import *
from crispy_forms.helper import FormHelper

class NewsletterUserSignUpForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_show_labels = False
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

class NewsletterCreationForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['subject', 'body', 'email', 'status']