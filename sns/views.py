from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Message, Group, Good
from .forms import SearchForm, PostForm
from django.contrib.auth.decorators import login_required


# indexのビュー関数
# @login_required(login_url='/admin/login/')
def index(request):

    # POST送信時の処理
    if request.method == 'POST':
        # フォームの用意
        searchform = SearchForm(request.POST)
        messages = get_message(request.POST['search'])

    # GETアクセス時の処理
    else:
        # フォームの用意
        searchform = SearchForm()
        messages = get_message(None)

    # 共通処理
    params = {
            'login_user': request.user,
            'contents': messages,
            'search_form': searchform,
        }
    return render(request, 'sns/index.html', params)


# メッセージのポスト処理
@login_required(login_url='/admin/login/')
def post(request):
    # POST送信の処理
    if request.method == 'POST':
        # 送信内容の取得
        # gr_name = request.POST['groups']
        content = request.POST['content']
        # Groupの取得
        # group = Group.objects.filter(owner=request.user).filter(title=gr_name).first()
        # if group == None:
        (pub_user, group) = get_public()
        # Messageを作成し設定して保存
        msg = Message()
        msg.owner = request.user
        msg.group = group
        msg.content = content
        msg.save()
        # メッセージを設定
        messages.success(request, '新しいメッセージを投稿しました！')
        return redirect(to='/sns')
    
    # GETアクセス時の処理
    else:
        form = PostForm(request.user)
    
    # 共通処理
    params = {
            'login_user':request.user,
            'form':form,
        }
    return render(request, 'sns/post.html', params)

# 投稿をシェアする
@login_required(login_url='/admin/login/')
def share(request, share_id):
    # シェアするMessageの取得
    share = Message.objects.get(id=share_id)
    
    # POST送信時の処理
    if request.method == 'POST':
        # 送信内容を取得
        # gr_name = request.POST['groups']
        content = request.POST['content']
        # Groupの取得
        # group = Group.objects.filter(owner=request.user) \
        #         .filter(title=gr_name).first()

        # if group == None:
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
        return redirect(to='/sns')
    
    # 共通処理
    form = PostForm(request.user)
    params = {
            'login_user':request.user,
            'form':form,
            'share':share,
        }
    return render(request, 'sns/share.html', params)


# goodボタンの処理
@login_required(login_url='/admin/login/')
def good(request, good_id):
    # goodするMessageを取得
    good_msg = Message.objects.get(id=good_id)
    # 自分がメッセージにGoodした数を調べる
    is_good = Good.objects.filter(owner=request.user) \
            .filter(message=good_msg).count()
    # ゼロより大きければ既にgood済み
    if is_good > 0:
        messages.success(request, '既にメッセージにはGoodしています。')
        return redirect(to='/sns')
    
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
    return redirect(to='/sns')


def get_message(find):

    if find is None:
        msgs = Message.objects.all()[:100]
    else:
        msgs = Message.objects.filter(content__contains=find)[:100]
    return msgs


# publicなUserとGroupを取得する
def get_public():
    public_user = User.objects.filter(username='public').first()
    public_group = Group.objects.filter \
            (owner=public_user).first()
    return (public_user, public_group)


