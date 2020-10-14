from .models import TComment
from django import forms

class CommentForm(forms.Form):
    parent = forms.IntegerField(required=True)
    targetUserId = forms.IntegerField(required=True)
    class Meta:
        model=TComment
        fields = ['body','article','user']