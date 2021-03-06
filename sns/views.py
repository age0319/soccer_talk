from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Message, Good
from .forms import SearchForm, PostForm, SignUpForm

import json
import pandas as pd

import os


def top(request):
    return render(request, 'sns/top.html')


def find(request):

    # POST送信時の処理
    if request.method == 'POST':

        form = SearchForm(request.POST)
        keyword = request.POST['keyword']
        # 投稿内容もしくはユーザ名を検索する
        result = Message.objects.filter(Q(content__contains=keyword) | Q(owner__username__contains=keyword))
        params = {
            'login_user': request.user,
            'contents': result,
            'form': form,
        }

    # GETアクセス時の処理
    else:
        form = SearchForm()

        params = {
            "form": form
        }

    return render(request, 'sns/find.html', params)


def board(request, num=1):

    msgs = Message.objects.all()
    page = Paginator(msgs, 10)

    # 共通処理
    params = {
            'login_user': request.user,
            'contents': page.get_page(num),
            'page': page.page_range,
            'page_active': num,          # intデータ
            'page_last': page.num_pages  # intデータ
        }

    return render(request, 'sns/board.html', params)


# メッセージのポスト処理
@login_required
def post(request):
    # POST送信の処理
    if request.method == 'POST':
        # 投稿内容の取得
        content = request.POST['content']

        # Messageを作成し設定して保存
        msg = Message()
        msg.owner = request.user
        msg.content = content
        msg.save()

        # メッセージを設定
        messages.success(request, '新しいメッセージを投稿しました！')
        return redirect(to='/sns/board')
    
    # GETアクセス時の処理
    else:
        form = PostForm(request.user)
    
    # 共通処理
    params = {
            'login_user': request.user,
            'form': form,
        }
    return render(request, 'sns/post.html', params)


# goodボタンの処理
@login_required
def good(request, good_id):
    # goodするMessageを取得
    good_msg = Message.objects.get(id=good_id)
    # 自分がメッセージにGoodした数を調べる
    is_good = Good.objects.filter(owner=request.user).filter(message=good_msg).count()
    # ゼロより大きければ既にgood済み
    if is_good > 0:
        messages.success(request, '既にメッセージにはGoodしています。')
        return redirect(to='/sns/board')
    
    # Messageのgood_countを１増やす
    good_msg.good_count += 1
    good_msg.save()
    # Goodを作成し、設定して保存
    good = Good()
    good.owner = request.user
    good.message = good_msg
    good.save()
    # メッセージを設定
    messages.success(request, 'メッセージにGoodしました！')
    return redirect(to='/sns/board')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(to='/sns/board')
    else:
        form = SignUpForm()
    return render(request, 'sns/signup.html', {'form': form})


UPLOAD_DIR = os.path.dirname(os.path.abspath(__file__)) + '/static/files/'


def news(request):

    # 表示する記事の数
    show_num = 10
    path = os.path.join(UPLOAD_DIR, "news.json")

    with open(path, 'r') as f:
        entries = json.load(f)

    params = {
        "entries": entries[:show_num]
    }

    return render(request, 'sns/news.html', params)


def ranking(request):

    path = os.path.join(UPLOAD_DIR, "ranking.csv")

    df = pd.read_csv(path)
    df = df.dropna(axis=1, how='any')

    # FOR TABLE <th> の文字列を真ん中にする
    pd.set_option('colheader_justify', 'center')

    params = {
        "table": df.to_html(classes='rank_table', index=False)
    }

    return render(request, 'sns/ranking.html', params)
