from django.shortcuts import render,redirect
from .models import Article,Link,Message,Diary
from comment.models import TComment
from django.db.models import Count
import pickle
from comment.forms import CommentForm
from .models import User
# Create your views here.
from django_redis import get_redis_connection
from django.views.decorators.cache import cache_page


def index(request):
    RedisConnection = get_redis_connection('default')
    try:
        articles = pickle.loads(RedisConnection.get('hotarticle'))
    except TypeError:
        articles = Article.objects.values().order_by('-read')[0:3]
        RedisConnection.set('hotarticle',pickle.dumps(articles),24*60*60)
    context = {'articles':articles}
    return render(request,'index.html',context)


def read(request,id):
    article = Article.objects.get(id=id) #单独获取年月日的操作在前端实现
    article.read += 1
    article.save()
    comments = TComment.objects.filter(article_id=id).values('body','createtime','user__username','id','reply_to__username','parent_id','user_id')
    pcomments = comments.filter(parent_id__isnull=True)
    ccomments = comments.filter(parent_id__isnull=False)
    url = request.get_full_path()
    error = ''
    error2= ''
    key = request.GET.get('key')
    if key == '1':
        error = '输入内容不能为空'
    elif key == '2':
        error2 = '输入内容不能为空'
    context = {'article': article,'ccomments':ccomments,'pcomments':pcomments,'url': url,'error':error,'error2':error2}
    return render(request,'read.html',context)

def article(request):
    # 取出所有博客文章
    articles = Article.objects.annotate(comment_count = Count('article_comment')).values('title','create','update','body','label','state','read','comment_count','id','picture_url','know')
    key = request.GET.get('key')
    if key:
        articles = articles.filter(label=key)
    # 需要传递给模板（templates）的对象
    hots,recommend = Article.objects.values('id','title').order_by('-read'),Article.objects.values('id','title').order_by('-update')
    hots,recommend = hots[0:4],recommend[0:4]
    context = {'articles': articles,'hots':hots,'recommend':recommend}
    # render函数：载入模板，并返回context对象
    return render(request,'article.html',context)
def diary(request):
    con = get_redis_connection('default')
    try:
        diarys = pickle.loads(con.get('diarys'))
    except TypeError:
        diarys = Diary.objects.values()
        con.set('diarys',pickle.dumps(diarys),5*60)
    context = {'diarys':diarys}
    return render(request,'diary.html',context)
def link(request):
    links = Link.objects.all()
    context = {'links':links}
    return render(request,'link.html',context)
def message(request):
    RedisConnection = get_redis_connection('default')
    if request.method == 'GET':
        error = ''
        key = request.GET.get('key')
        if key:
            error = '留言内容不能为空'
        try:
            messages = pickle.loads(RedisConnection.get('message_list'))
        except TypeError:
            messages = Message.objects.values('body','create','user__username').order_by('-create')
            RedisConnection.set('message_list',pickle.dumps(messages),6*60*60)
        context = {'messages':messages,'error':error}
    elif request.method == 'POST':
        data = request.POST
        if data['message_body']:
            body,user = data['message_body'],request.session.get('_auth_user_id')
            Message.objects.create(user_id=user,body=body)
            RedisConnection.delete('message_list')
            return redirect('/message/')
        else:
            return redirect('/message/?key=1')
    return render(request,'message.html',context)

def about(request):
    links = Link.objects.all()
    context = {'links': links}
    return render(request,'about.html',context)