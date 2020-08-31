from django import forms
from django.contrib.auth.models import User


class UserLogin(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class UserRegister(forms.ModelForm):
    password = forms.CharField(max_length=20,
                               min_length=6,
                               error_messages={'required':'请填入密码','max_length':'密码需小于20位','min_length':'密码最少六位'})
    password2 = forms.CharField(max_length=20,
                                min_length=6,
                                error_messages={'required':'请填入密码','max_length':'密码需小于20位','min_length':'密码最少六位'})
    class Meta:
        model = User
        fields = ('username','email')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username=username)
        if len(username) <6 or len(username) >12:
            raise forms.ValidationError('请输入6-12位的用户名')
        elif user:
            raise forms.ValidationError('用户名已存在，请重试。')
        else:
            return username

    # 对两次输入的密码是否一致进行检查
    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError("密码输入不一致,请重试。")