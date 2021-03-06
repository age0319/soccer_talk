from django import forms
from django.contrib.auth.forms import UserCreationForm


# ユーザ作成フォームのカスタム
class SignUpForm(UserCreationForm):
    username = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)


# 検索フォーム
class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=100)


# 投稿フォーム
class PostForm(forms.Form):
    content = forms.CharField(max_length=300, widget=forms.Textarea(attrs={'rows': 8}))
    
    def __init__(self, user, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
