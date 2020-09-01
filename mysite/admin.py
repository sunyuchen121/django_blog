from django.contrib import admin

# Register your models here.

from . import models
admin.site.register(models.user)#在后台中添加对user表的操作
admin.site.register(models.Article)
admin.site.register(models.Link)
admin.site.register(models.Diary)