from django.shortcuts import render,redirect

# Create your views here.
from comment import models
from django.contrib.auth.decorators import login_required

@login_required
def comment(request):
    if request.method == 'POST':
        data = request.POST
        if data['body']:
            article,user,body = data['article_id'],request.session.get('_auth_user_id'),data['body']
            models.Comment.objects.create(article_id=article,user_id=user,body=body)
            return redirect('/read/'+article)
        else:
            article = data['article_id']
            return redirect('/read/' + article+'/?key=1')