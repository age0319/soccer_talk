from django import forms


class FindForm(forms.Form):
    find = forms.CharField(max_length=50)


class MessageForm(forms.Form):
    content = forms.CharField(max_length=500, widget=forms.Textarea)
