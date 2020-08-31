from django.db import models

# Create your models here.
from mysite.models import Article
from django.contrib.auth.models import User

class Comment(models.Model):
    article = models.ForeignKey(Article,on_delete=models.CASCADE,related_name='article_comment')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='my_comment')
    createtime = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    class Meta:
        ordering = ['createtime']



