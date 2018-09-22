from django.shortcuts import render
from .forms import FriendForm
from .models import Friend
from django.shortcuts import redirect
from .forms import FindForm


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


def edit(request, num):
    obj = Friend.objects.get(id=num)
    if request.method == 'POST':
        friend = FriendForm(request.POST, instance=obj)
        friend.save()
        return redirect(to='/hello')
    params = {
        'title': 'Hello',
        'id': num,
        'form': FriendForm(instance=obj),
    }
    return render(request, 'hello/edit.html', params)


def delete(request, num):
    friend = Friend.objects.get(id=num)
    if request.method == 'POST':
        friend.delete()
        return redirect(to='/hello')
    params = {
        'title': 'Hello',
        'id': num,
        'obj': friend
    }
    return render(request, 'hello/delete.html', params)


def find(request):
    if request.method == 'POST':
        msg = 'search result'
        form = FindForm(request.POST)
        str = request.POST['find']
        list = str.split()
        data = Friend.objects.filter(name__in=list)
    else:
        msg = 'what do you like to search?'
        form = FindForm()
        data = Friend.objects.all()

    params = {
        'title': 'Hello',
        'msg': msg,
        'form': form,
        'data': data
    }
    return render(request, 'hello/find.html', params)