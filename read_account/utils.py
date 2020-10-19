from django.contrib.contenttypes.models import ContentType
from .models import ReadNum

def read_account_once(request,obj):

    tarmodel = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (tarmodel.model,obj.pk)

    if not request.COOKIES.get(key):
    
        if ReadNum.objects.filter(content_type=tarmodel,object_id=obj.pk).count():
            readnum = ReadNum.objects.get(content_type=tarmodel,object_id=obj.pk)
        else:
            readnum = ReadNum(content_type=tarmodel,object_id=obj.pk)

        readnum.read_num += 1
        readnum.save()
    return key