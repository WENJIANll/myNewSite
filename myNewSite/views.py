import datetime
from django.shortcuts import render_to_response
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType
from read_account.utils import get_sevendays_date,get_today_hot,get_yestody_hotdata
from blog.models import Blog


# Create your views here.

def get7hotdata():
    today = timezone.now().date()
    sevenday = today - datetime.timedelta(days=7)
    blogs = Blog.objects \
                .filter(read_details__date__lt=today,read_details__date__gt=sevenday) \
                .values('id','title') \
                .annotate(read_group_num=Sum('read_details__read_num')) \
                .order_by('-read_group_num')
    return blogs


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates,read_nums = get_sevendays_date(blog_content_type)
    today_hot_data = get_today_hot(blog_content_type)
    yes_hot_data = get_yestody_hotdata(blog_content_type)
    # seven_hotdata = get_seven_hotdata(blog_content_type)

    # 获取七天热门的缓存
    seven_hotdata = cache.get('seven_hotdata')
    if seven_hotdata is None:
        seven_hotdata = get7hotdata()
        cache.set('seven_hotdata',seven_hotdata,3600)
        print('jisuan cach')
    else:
        print('shiyong cach')

    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_data']  = today_hot_data
    context['yes_hot_data']  = yes_hot_data
    # context['seven_hotdata']  = seven_hotdata
    context['seven_hotdata']  = seven_hotdata

    return render_to_response('home.html',context)

