from django import forms
from tinymce import TinyMCE
from ckeditor.widgets import CKEditorWidget
from .models import Post, Comment


# class TinyMCEWidget(TinyMCE):
#     def use_required_attribute(self, *args):
#         return False


class PostForm(forms.ModelForm):
    # content = forms.CharField(
    #     widget=TinyMCEWidget(
    #         attrs={'required': False, 'cols': 30, 'rows': 10}
    #     )
    # )
    content = forms.CharField(
        widget=CKEditorWidget(
        attrs={'required': False, 'cols': 30, 'rows': 10}
    ))
    class Meta:
        model = Post
        fields = ('title', 'slug', 'content', 'thumbnail', 'previous_post', 'next_post', 'category', 'tags')


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type your comment',
        'id': 'usercomment',
        'rows': '3'
    }))
    class Meta:
        model = Comment
        fields = ('content', )