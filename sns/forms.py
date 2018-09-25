from django import forms


# 検索フォーム
class SearchForm(forms.Form):
    search = forms.CharField(max_length=100)

# 投稿フォーム
class PostForm(forms.Form):
    content = forms.CharField(max_length=500, widget=forms.Textarea)
    
    def __init__(self, user, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
