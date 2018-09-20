from django.shortcuts import render
from .forms import FriendForm
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

    if request.method == 'POST':
        obj = Friend()
        friend = FriendForm(request.POST, instance=obj)
        friend.save()
        return redirect(to='/hello')

    params = {
        'title': 'Hello',
        'form': FriendForm(),
    }
    return render(request, 'hello/create.html', params)

