from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Message, Group, Good
from .forms import SearchForm, PostForm, UserCreateForm2
from django.contrib.auth.decorators import login_required

from django.contrib.auth import login
import feedparser
import json
from django.core.paginator import Paginator


# indexのビュー関数
def index(request, num=1):

    # POST送信時の処理
    if request.method == 'POST':
        # フォームの用意
        searchform = SearchForm(request.POST)
        find = request.POST['search']
        msgs = Message.objects.filter(content__contains=find)
        params = {
            'login_user': request.user,
            'contents': msgs,
            'search_form': searchform,
        }

    # GETアクセス時の処理
    else:
        # フォームの用意
        searchform = SearchForm()
        msgs = Message.objects.all()
        page = Paginator(msgs, 10)

        # 共通処理
        params = {
                'login_user': request.user,
                'contents': page.get_page(num),
                'search_form': searchform,
            }

    return render(request, 'sns/index.html', params)


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
        (pub_user, group) = get_public()
        msg.group = group
        msg.content = content
        msg.save()

        # メッセージを設定
        messages.success(request, '新しいメッセージを投稿しました！')
        return redirect(to='/sns/index')
    
    # GETアクセス時の処理
    else:
        form = PostForm(request.user)
    
    # 共通処理
    params = {
            'login_user': request.user,
            'form': form,
        }
    return render(request, 'sns/post.html', params)


# 投稿をシェアする
@login_required
def share(request, share_id):
    # シェアするMessageの取得
    share = Message.objects.get(id=share_id)
    
    # POST送信時の処理
    if request.method == 'POST':
        # 送信内容を取得
        content = request.POST['content']
        (pub_user, group) = get_public()

        # メッセージを作成し、設定をして保存
        msg = Message()
        msg.owner = request.user
        msg.group = group
        msg.content = content
        msg.share_id = share.id
        msg.save()
        share_msg = msg.get_share()
        share_msg.share_count += 1
        share_msg.save()
        # メッセージを設定
        messages.success(request, 'メッセージをシェアしました！')
        return redirect(to='/sns/index')
    
    # 共通処理
    form = PostForm(request.user)
    params = {
            'login_user': request.user,
            'form': form,
            'share': share,
        }
    return render(request, 'sns/share.html', params)


# goodボタンの処理
@login_required
def good(request, good_id):
    # goodするMessageを取得
    good_msg = Message.objects.get(id=good_id)
    # 自分がメッセージにGoodした数を調べる
    is_good = Good.objects.filter(owner=request.user) \
            .filter(message=good_msg).count()
    # ゼロより大きければ既にgood済み
    if is_good > 0:
        messages.success(request, '既にメッセージにはGoodしています。')
        return redirect(to='/sns/index')
    
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
    return redirect(to='/sns/index.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreateForm2(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(to='/sns/index')
    else:
        form = UserCreateForm2()
    return render(request, 'sns/signup.html', {'form': form})


def test(request):
    return render(request, 'sns/test.html')


def news(request):

    # 表示する記事の数
    show_num = 10

    # 記事データを取得する
    do_scrape()

    with open("news.json", 'r') as f:
        entries = json.load(f)

    params = {
        "entries": entries[:show_num]
    }

    return render(request, 'sns/news.html', params)


def ranking(request):
    pass


# 以下普通の関数


def do_scrape():

    # 取得する記事の数、最大で20個
    entry_num = 20

    url = "https://news.google.com/news/rss/search/section/q/j2%e3%83%aa%e3%83%bc%e3%82%b0/j2%e3%83%aa%e3%83%bc%e3" \
          "%82%b0?ned=jp&hl=ja&gl=JP"

    d = feedparser.parse(url)
    news = list()

    for i, entry in enumerate(d.entries[:entry_num], 1):
        p = entry.published_parsed
        sortkey = "%04d%02d%02d%02d%02d%02d" % (p.tm_year, p.tm_mon, p.tm_mday, p.tm_hour, p.tm_min, p.tm_sec)

        tmp = {
            "no": i,
            "title": entry.title,
            "link": entry.link,
            "published": entry.published,
            "sortkey": sortkey
        }

        news.append(tmp)

    news = sorted(news, key=lambda x: x['sortkey'], reverse=True)

    with open('news.json', 'w') as f:
        json.dump(news, f)


def get_message(find):

    if find is None:
        msgs = Message.objects.all()[:100]
    else:
        msgs = Message.objects.filter(content__contains=find)[:100]
    return msgs


# publicなUserとGroupを取得する
def get_public():
    public_user = User.objects.filter(username='public').first()
    public_group = Group.objects.filter(owner=public_user).first()
    return public_user, public_group


