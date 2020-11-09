from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from mdeditor.fields import MDTextField
from ckeditor_uploader.fields import RichTextUploadingField
from read_account.models import ReadNumExpand,ReadDetail
from comment.models import Comment

class BlogType(models.Model):
    type_name = models.CharField(max_length=15)
    desc = MDTextField(default='正在想')

    """docstring for BlogType"""
    def __str__(self):
    	return self.type_name

class Blog(models.Model,ReadNumExpand):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType,on_delete=models.CASCADE,related_name = 'blog_blog')
    content = MDTextField()
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    read_details = GenericRelation(ReadDetail)
    # readed_num = models.IntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    

    def __str__(self):
    	return "<Blog: %s>" % self.title

    class Meta:
        ordering = ['created_time']
    
    def get_comment_num(self):

        blog_content_type = ContentType.objects.get_for_model(self)

        comments = Comment.objects.filter(content_type=blog_content_type,object_id=self.pk)
        L = len(comments)
        return L


'''
    def get_read_num(self):
        try:
            return self.readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0 
'''

'''
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    blog = models.OneToOneField(Blog, on_delete=models.CASCADE)
'''

   






    