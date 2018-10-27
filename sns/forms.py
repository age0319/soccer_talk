from django import forms
from django.contrib.auth.forms import UserCreationForm


# ユーザ作成フォームのカスタム
class UserCreateForm2(UserCreationForm):
    username = forms.CharField(label="ユーザ名")
    password1 = forms.CharField(label="パスワード", widget=forms.PasswordInput)
    password2 = forms.CharField(label="パスワードの確認", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserCreateForm2, self).__init__(*args, **kwargs)


# 検索フォーム
class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=100, label="")

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)


# 投稿フォーム
class PostForm(forms.Form):
    content = forms.CharField(max_length=300, widget=forms.Textarea(attrs={'rows': 8}), label="")
    
    def __init__(self, user, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
