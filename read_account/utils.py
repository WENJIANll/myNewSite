import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from .models import ReadNum,ReadDetail



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


