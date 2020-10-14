from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.
from mysite.models import Article
from django.contrib.auth.models import User
from mptt.models import TreeForeignKey,MPTTModel

class Cccomment(models.Model):
    article = models.ForeignKey(Article,on_delete=models.CASCADE,related_name='article_comment')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='my_comment')
    createtime = models.DateTimeField(auto_now_add=True)
    body = RichTextField()
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='child')
    reply_to = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='cdreply')
    class Meta:
        ordering = ['createtime']


class TComment(MPTTModel):
    # 发表评论的用户
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_comments')
    # 父评论,如果本评论为父评论,该字段就为空
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child_comments')
    # 评论给谁,如果本评论为父评论,该字段就为空,后面会用到
    reply_to = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='replytome')
    # 评论内容
    body = models.TextField()
    # 评论时间
    create = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ['-create']




