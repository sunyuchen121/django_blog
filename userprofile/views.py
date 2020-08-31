from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
# Create your views here.
from userprofile import forms
from django.contrib.auth import authenticate,login,logout

def UserLogin(request):
    #判断用户是否提交数据
    if request.method == 'POST':
        data = request.POST
        #将提交的数据赋值给表单实例
        user_info = forms.UserLogin(data)
        #判断提交的数据是否满足模型的要求
        if user_info.is_valid():
            #cleaned_data中的值类型与字段定义的Field类型一致
            data = user_info.cleaned_data
            # 保存数据，但暂时不提交到数据库中
            # 检验账号、密码是否正确匹配数据库中的某个用户
            # 如果均匹配则返回这个 user 对象
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                # 将用户数据保存在 session 中，即实现了登录动作
                login(request,user)
                return redirect('/index/')
            else:
                return HttpResponse('账号或密码输入错误')
        else:
            return HttpResponse("账号或密码输入不合法")
    # 如果用户请求获取登陆界面
    elif request.method == 'GET':
        # 创建表单类实例
        user_info = forms.UserLogin()
        context = {'user_info':user_info}
        return render(request,'login.html',context)
    else:
        return HttpResponse("请使用GET或POST请求数据")


def register(request):
    if request.method == 'POST':
        data = request.POST
        user_info = forms.UserRegister(data)
        if user_info.is_valid():
            new_user = user_info.save(commit=False)
            new_user.set_password(user_info.cleaned_data['password'])
            new_user.save()
            return redirect('/userprofile/login/')
        else:
            error = user_info.errors
            return render(request,'register.html',{'error':error})
    elif request.method =='GET':
        user_info = forms.UserRegister()
        context = {'user_info':user_info}
        return render(request,'register.html',context)

def Userlogout(request):
    if request.session:
        logout(request)
        return redirect('/index/')