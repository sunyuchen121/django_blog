from django.shortcuts import render,redirect
from .models import Article,Link,Message
from comment.models import Comment
from django.db.models import Count
# Create your views here.

def index(request):
    return render(request,'index.html')
def read(request,id):
    article = Article.objects.get(id = id)
    article.read += 1
    article.save()
    comments = Comment.objects.filter(article_id=id).values()
    url = request.get_full_path()
    context = {'article':article,'comments':comments,'url':url}

    return render(request,'read.html',context)
def article(request):
    # 取出所有博客文章
    articles = Article.objects.annotate(comment_count = Count('article_comment')).values('title','create','update','body','label','state','read','comment_count','id')
    key = request.GET.get('key')
    if key:
        articles = Article.objects.filter(label=key).annotate(comment_count = Count('article_comment')).values('title','create','update','body','label','state','read','comment_count','id')
    # 需要传递给模板（templates）的对象
    context = {'articles': articles}
    # render函数：载入模板，并返回context对象
    return render(request,'article.html',context)
def diary(request):
    return render(request,'diary.html')
def link(request):
    links = Link.objects.all()
    context = {'links':links}
    return render(request,'link.html',context)
def message(request):
    if request.method == 'GET':
        messages = Message.objects.values('body','create','user__username')
        context = {'messages':messages}
    elif request.method == 'POST':
        data = request.POST
        body,user = data['message_body'],request.session.get('_auth_user_id')
        Message.objects.create(user_id=user,body=body)
        return redirect('/message/')
    return render(request,'message.html',context)
def about(request):
    return render(request,'about.html')