from django import forms
from .models import *


class CreateMovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'
        
class MovieReviewForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type your comment',
        'id': 'usercomment',
        'rows': '6'
    }))
    class Meta:
        model = Review
        fields = '__all__'
        exclude = ['user', 'movie']