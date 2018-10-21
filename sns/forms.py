from django import forms
from django.contrib.auth.forms import UserCreationForm


# ユーザ作成フォームのカスタム
class UserCreateForm2(UserCreationForm):
    username = forms.CharField(label="ユーザ名")
    password1 = forms.CharField(label="パスワード")
    password2 = forms.CharField(label="パスワードの確認")

    def __init__(self, *args, **kwargs):
        super(UserCreateForm2, self).__init__(*args, **kwargs)

        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].help_text = None

        self.fields['password1'].help_text = "パスワードは4文字以上にして下さい。"


# 検索フォーム
class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, label="検索したい文字")


# 投稿フォーム
class PostForm(forms.Form):
    content = forms.CharField(max_length=300, widget=forms.Textarea, label="投稿内容")
    
    def __init__(self, user, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
