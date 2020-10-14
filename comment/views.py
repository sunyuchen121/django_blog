from django.shortcuts import render,redirect

# Create your views here.
from comment import models
from django.contrib.auth.decorators import login_required

@login_required
def comment(request):
    if request.method == 'POST':
        data = request.POST
        if data['body']:
            article_id,parent,reply_to,body,user = data['article_id'],data.get('parent'),data.get('targetUserId'),data['body'],request.session.get('_auth_user_id')
            models.Comment.objects.create(article_id=article_id,parent_id=parent,reply_to_id=reply_to,user_id=user,body=body)
            return redirect('/read/' + article_id)
        elif not data['body'] and not 'parent' in data:
            article = data['article_id']
            return redirect('/read/' + article + '/?key=1')
        elif not data['body'] and 'parent' in data:
            article = request.POST['article_id']
            return redirect('/read/' + article + '/?key=2')