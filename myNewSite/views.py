import datetime
from django.shortcuts import render,redirect
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.auth.models import User

from read_account.utils import get_sevendays_date,get_today_hot,get_yestody_hotdata
from blog.models import Blog,BlogType
from user.forms import LoginForm,RegForm


# Create your views here.

def get7hotdata():
    today = timezone.now().date()
    sevenday = today - datetime.timedelta(days=7)
    blogs = Blog.objects \
                .filter(read_details__date__lt=today,read_details__date__gt=sevenday) \
                .values('id','title') \
                .annotate(read_group_num=Sum('read_details__read_num')) \
                .order_by('-read_group_num')
    return blogs[:7]


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates,read_nums = get_sevendays_date(blog_content_type)
    today_hot_data = get_today_hot(blog_content_type)
    yes_hot_data = get_yestody_hotdata(blog_content_type)
    # seven_hotdata = get_seven_hotdata(blog_content_type)

    # 获取七天热门的缓存
    seven_hotdata = cache.get('seven_hotdata')[:7]
    if seven_hotdata is None:
        seven_hotdata = get7hotdata()
        cache.set('seven_hotdata',seven_hotdata,3600)
        print('jisuan cach')
    else:
        pass
    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_data']  = today_hot_data
    
    context['yes_hot_data']  = yes_hot_data
    # context['seven_hotdata']  = seven_hotdata
    context['seven_hotdata']  = seven_hotdata

    return render(request,'home.html',context)
'''
def loginn(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)

    
    
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = authenticate(request, username=username, password=password)
    # 获取登陆前的页面
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    if user is not None:
        login(request, user)
        return redirect(referer)
        # Redirect to a success page.
        
    else:
        # Return an 'invalid login' error message.
        
        return render(request,'error.html',{'message':'用户名或密码不正确'})

def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # 创建用户
            user = User.objects.create_user(username, email, password)
            user.save()
            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        reg_form = RegForm()

    context = {}
    context['reg_form'] = reg_form
    return render(request, 'register.html', context)
    '''

