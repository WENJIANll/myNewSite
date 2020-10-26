from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment,Likes,Likes_count
from ..forms import CommentForm


register = template.Library()

@register.simple_tag
def get_comment_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=content_type, object_id=obj.pk).count()

@register.simple_tag
def get_comment_form(obj):
    content_type = ContentType.objects.get_for_model(obj)
    form = CommentForm(initial={
            'content_type': content_type.model, 
            'object_id': obj.pk, 
            'reply_comment_id': 0})
    return form

@register.simple_tag
def get_comment_list(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(content_type=content_type, object_id=obj.pk, parent=None)
    return comments.order_by('-comment_time')

@register.simple_tag(takes_context=True)
def get_like_status(context, obj):
    content_type = ContentType.objects.get_for_model(obj)
    user = context['user']
    if not user.is_authenticated:
        return ''
    if Likes.objects.filter(content_type=content_type, object_id=obj.pk, usermakelike=user).exists():
        return 'active'
    else:
        return ''

@register.simple_tag
def get_like_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    like_count, created = Likes_count.objects.get_or_create(content_type=content_type, object_id=obj.pk)
    return like_count.like_count

@register.simple_tag
def get_content_type(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return content_type.model