from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import HelloForm
from .models import Friend


def index(request):

    params = {
        'title': 'Hello',
        'massage': 'all friends',
        'form': HelloForm(),
        'data': []
    }

    if request.method == 'POST':
        num = request.POST['id']
        item = Friend.objects.get(id=num)
        params['data'] = [item]
        params['form'] = HelloForm()
    else:
        params['data'] = Friend.objects.all()

    return render(request, 'hello/index.html', params)




class HelloView(TemplateView):

    def __init__(self):
        self.params = {
            'title': 'Hello',
            'message': 'your data',
            'form': HelloForm()
        }

    def get(self, request):
        return render(request, 'hello/index.html', self.params)

    def post(self, request):
        msg = 'あなたは、<b>' + request.POST['name'] + \
            '(' + request.POST['age'] + ') </b> さんです' + \
            '<br>メールアドレスは<b>' + request.POST['mail'] + '</b>でござろう。'

        self.params['message'] = msg
        self.params['form'] = HelloForm(request.POST)

        return render(request, 'hello/index.html', self.params)
