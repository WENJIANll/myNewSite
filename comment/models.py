from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

# Create your models here.
class Comment(models.Model):

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # 记录对应模型的主键值
    object_id = models.PositiveIntegerField()
    # 将上面两个变为通用的外键
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # 這裏雖然這麽設置成了root，那他就是root嗎？在哪裏把他當作root的
    root = models.ForeignKey('self', related_name='root_comment', null=True, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='parent_comment', null=True, on_delete=models.CASCADE)
    # related_name 是從User反向找到該User有哪些comment的方法
    reply_to = models.ForeignKey(User, related_name="replies", null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-comment_time']

class Likes(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # 记录对应模型的主键值
    object_id = models.PositiveIntegerField()
    # 将上面两个变为通用的外键
    content_object = GenericForeignKey('content_type', 'object_id')
    usermakelike = models.ForeignKey(User,related_name="usermakelike", on_delete=models.CASCADE)
    # related_name 是從User反向找到該User有哪些likes_for的方法
    likes_for = models.ForeignKey(User, related_name="likes_for", null=True, on_delete=models.CASCADE)
    is_like = models.BooleanField(default=True)
    like_time = models.DateTimeField(auto_now_add=True)
    
class Likes_count(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # 记录对应模型的主键值
    object_id = models.PositiveIntegerField()
    # 将上面两个变为通用的外键
    content_object = GenericForeignKey('content_type', 'object_id')
    like_count = models.IntegerField(default=0)
