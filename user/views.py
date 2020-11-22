import string
import random
import time
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.mail import send_mail
from django.http import JsonResponse
from .forms import LoginForm, RegForm,ChangeNicknameform,BindEmailForm,Change_passwordForm,ForgotPasswordForm
from .models import Profile


def login_for_medal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)

def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'user/login.html', context)

def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST,request=request)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # 创建用户
            user = User.objects.create_user(username, email, password)
            user.save()
            del request.session['register_code']
            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        reg_form = RegForm()

    context = {}
    context['reg_form'] = reg_form
    return render(request, 'user/register.html', context)
    
def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))

def user_info(request):
    context = {}
    return render(request, 'user/user_info.html', context)

def change_nickname(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        # 传user是为了给form绑定上是哪个用户要改昵称
        form = ChangeNicknameform(request.POST,user=request.user)
        if form.is_valid() :
            new_nickname = form.cleaned_data['new_nickname']
            # 创建profile，是否创建
            profile,created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = new_nickname
            profile.save()
            return redirect(redirect_to)
    else:
        change_nickname_form =  ChangeNicknameform()
    context = {}
    context['page_title'] = '修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '修改'
    context['form'] = change_nickname_form
    context['return_back_url'] = redirect_to
    
    return render(request,'form.html',context)

def bind_email(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = BindEmailForm(request.POST,request=request)
        if form.is_valid() :
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            del request.session['bindemailcode']
            return redirect(redirect_to)
    else:
        form =  BindEmailForm()
    context = {}
    context['page_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '绑定'
    context['form'] = form
    context['return_back_url'] = redirect_to
    
    return render(request,'user/bind_email.html',context)

# 这个是发送验证码按钮通用的校验方法
def send_vertifycode(request):
    email = request.GET.get('email','')
    send_type = request.GET.get('send_type','')
    data = {}
    if email != '':
        # 生成验证码
        code = ''.join(random.sample(string.ascii_letters + string.digits,4))
        now = int(time.time())
        send_time = request.session.get('send_time',0)
        # now是距离标准时间的秒数，他和零之间的差距肯定是大于30的
        if now - send_time < 30:
            data['status'] = 'ERROR'
        else:
            # 设置session
            request.session[send_type] = code
            request.session['send_time'] = now

            # 发送邮件
            send_status = send_mail(
                '小破站的验证码',
                '验证码：%s' % code,
                '1305133324@qq.com',
                [email],
                fail_silently=False,
            )
            # if send_status:
            #     print('发送成功')
            # else:
            #     print('发送失败')

            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)

def change_password(request):
    redirect_to = request.GET.get('from', reverse('home'))

    if request.method == 'POST':
        form = Change_passwordForm(request.POST,request=request)
        if form.is_valid() :
            user = request.user
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            auth.logout(request)
            return redirect(redirect_to)
    else:
        form = Change_passwordForm()
    context = {}
    context['page_title'] = '修改密码'
    context['form_title'] = '修改密码'
    context['submit_text'] = '修改'
    context['form'] = form
    context['return_back_url'] = redirect_to
    
    return render(request,'form.html',context)
    
def forgot_password(request):
    redirect_to = reverse('login')
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            # 清除session
            del request.session['forgot_password_code']
            return redirect(redirect_to)
    else:
        form = ForgotPasswordForm()

    context = {}
    context['page_title'] = '重置密码'
    context['form_title'] = '重置密码'
    context['submit_text'] = '重置'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'user/forgot_password.html', context)