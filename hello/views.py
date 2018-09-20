from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import HelloForm
from .models import Friend
from django.shortcuts import redirect


def index(request):

    data = Friend.objects.all()

    params = {
        'title': 'Hello',
        'data': data
    }

    return render(request, 'hello/index.html', params)


def create(request):

    params = {
        'title': 'Hello',
        'form': HelloForm(),
    }

    if request.method == 'POST':
        name = request.POST['name']
        mail = request.POST['mail']
        gender = 'gender' in request.POST
        age = request.POST['age']
        birth = request.POST['birthday']

        friend = Friend(name=name, mail=mail, gender=gender, age=age, birthday=birth)
        friend.save()
        return redirect(to='/hello')

    return render(request, 'hello/create.html', params)


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
