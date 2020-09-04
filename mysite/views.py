from django.shortcuts import render,redirect
from .models import Article,Link,Message,Diary
from comment.models import Comment
from django.db.models import Count
from .models import User
# Create your views here.


def index(request):
    hot_article = Article.objects.values().order_by('-read')
    articles = hot_article[0:3]
    context = {'articles':articles}
    return render(request,'index.html',context)
def read(request,id):
    article = Article.objects.get(id=id) #单独获取年月日的操作在前端实现
    article.read += 1
    article.save()
    comments = Comment.objects.filter(article_id=id).values('body','createtime','user__username')
    url = request.get_full_path()
    error = ''
    key = request.GET.get('key')
    if key:
        error = '输入内容不能为空'
    context = {'article': article, 'comments': comments, 'url': url,'error':error}
    return render(request,'read.html',context)
def article(request):
    # 取出所有博客文章
    articles = Article.objects.annotate(comment_count = Count('article_comment')).values('title','create','update','body','label','state','read','comment_count','id','picture_url')
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
    diarys = Diary.objects.values()
    context = {'diarys':diarys}
    return render(request,'diary.html',context)
def link(request):
    links = Link.objects.all()
    context = {'links':links}
    return render(request,'link.html',context)
def message(request):
    if request.method == 'GET':
        error = ''
        key = request.GET.get('key')
        if key:
            error = '留言内容不能为空'
        messages = Message.objects.values('body','create','user__username')
        context = {'messages':messages,'error':error}
    elif request.method == 'POST':
        data = request.POST
        if data['message_body']:
            body,user = data['message_body'],request.session.get('_auth_user_id')
            Message.objects.create(user_id=user,body=body)
            return redirect('/message/')
        else:
            return redirect('/message/?key=1')
    return render(request,'message.html',context)
def about(request):
    links = Link.objects.all()
    context = {'links': links}
    return render(request,'about.html',context)