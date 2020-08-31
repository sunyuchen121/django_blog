from django.shortcuts import render,redirect

# Create your views here.
from comment import models

def comment(request):
    if request.method == 'POST':
        data = request.POST
        if data:
            article,user,body = data['article_id'],request.session.get('_auth_user_id'),data['body']
            comment = models.Comment.objects.create(article_id=article,user_id=user,body=body)
            return redirect('/read/'+article)