from django.shortcuts import render
from .forms import HelloForm


def index(request):
    params = {
        'title': 'Hello/Index',
        'message': 'your data',
        'form': HelloForm()
    }
    if request.method == 'POST':
        params['message'] = '名前:' + request.POST['name'] + \
                            '<br>メール:' + request.POST['mail'] + \
                            '<br>年齢:' + request.POST['age']
        params['form'] = HelloForm(request.POST)
    return render(request, 'hello/index.html', params)

