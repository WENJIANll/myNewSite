import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from .models import ReadNum,ReadDetail
from blog.models import Blog


def read_account_once(request,obj):

    tarmodel = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (tarmodel.model,obj.pk)

    if not request.COOKIES.get(key):
        # 总阅读数
        readnum,created = ReadNum.objects.get_or_create(content_type=tarmodel,object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()

        # 当天阅读数
        date = timezone.now().date()
        readdetail,created = ReadDetail.objects.get_or_create(content_type=tarmodel,object_id=obj.pk,date=date)
        readdetail.read_num += 1
        readdetail.save()
    return key

def get_sevendays_date(content_type):
    today = timezone.now().date()
    read_nums = []
    dates = []
    for i in range(7,-1,-1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_detail = ReadDetail.objects.filter(content_type=content_type,date=date)
        # 聚合函数
        result = read_detail.aggregate(readsum_of_num = Sum('read_num'))
        read_nums.append(result['readsum_of_num'] or 0)
    return dates,read_nums

def get_today_hot(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type,date=today).order_by('-read_num')
    return read_details[:7]

def get_yestody_hotdata(content_type):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    yes_read_details = ReadDetail.objects.filter(content_type=content_type,date=yesterday).order_by('-read_num')
    return yes_read_details[:7]

def get7hotdata():
    today = timezone.now().date()
    sevenday = today - datetime.timedelta(days=7)
    # values返回一个指定字段作为key的字典，而不是返回一个或一组实例对象
    # 然后使用annotate按照这个结果进行分组，并对指定字段求和
    # blogs = Blog.objects \
    #             .filter(read_details__date__lt=today,read_details__date__gt=sevenday) \
    #             .annotate(read_group_num=Sum('read_details__read_num')) \
    #             .order_by('-read_group_num')
    blogs = Blog.objects \
                .filter(read_details__date__lt=today,read_details__date__gt=sevenday) \
                .values('id','title') \
                .annotate(read_group_num=Sum('read_details__read_num')) \
                .order_by('-read_group_num')
    return blogs[:7]
    #获取30天的后面完善

def get_seven_hotdata(content_type):
    today = timezone.now().date()
    sevenday = today - datetime.timedelta(days=7)
    # values返回一个可迭代的字典集，annotate实现groupby
    '''
    seven_read_details = ReadDetail.objects \
                                   .filter(content_type=content_type,date__gt=sevenday) \
                                   .values('content_type','object_id') \
                                   .annotate(read_group_num=Sum('read_num')) \
                                   .order_by('-read_group_num')'''
    
    return seven_read_details[:7]

