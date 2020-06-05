from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *



class CreateUserForm(UserCreationForm):
    username = forms.CharField(label='Your Username')
    email = forms.EmailField(required=True, label='Your Email')
    password1 = forms.CharField(max_length=30, label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=30, label='Confirm Password', widget=forms.PasswordInput)
    
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            self.fields[field_name].widget.attrs.update({
                "placeholder": field.label,
                'class': "input100"
            })
            
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This email has already been registered")
        return email


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email']
        
        
class ProfileUdateForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['profile_picture']