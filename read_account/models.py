from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions


# Create your models here.

class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    # 外键模型
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # 记录对应模型的主键值
    object_id = models.PositiveIntegerField()
    # 将上面两个变为通用的外键
    content_object = GenericForeignKey('content_type', 'object_id')

class ReadNumExpand():
    def get_read_num(self):
        try:
            tarmodel = ContentType.objects.get_for_model(self)
            readnum = ReadNum.objects.get(content_type=tarmodel,object_id=self.pk)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0   