from django.contrib import admin
from .models import Comment,Likes,Likes_count

# Register your models here.

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content_object','text','comment_time','user','content_type')

@admin.register(Likes)
class LikesAdmin(admin.ModelAdmin):
    list_display = ('content_object','usermakelike','object_id','likes_for','content_type')


@admin.register(Likes_count)
class Likes_countAdmin(admin.ModelAdmin):
    list_display = ('content_object','like_count','object_id')
