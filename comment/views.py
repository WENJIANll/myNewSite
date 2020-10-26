from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.http import JsonResponse

from .models import Comment,Likes,Likes_count
from .forms import CommentForm



# Create your views here.

def update_comment(request):
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    comment_form = CommentForm(request.POST, user=request.user)
    data = {}

    if comment_form.is_valid():
        # 检查通过，保存数据
        comment = Comment()
        # cleaned_Data到底是幹嘛的<--用來校驗數據的
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']
        print(comment.content_type)
        print(comment.object_id)


        parent = comment_form.cleaned_data['parent']
        if not parent is None:
            comment.root = parent.root if not parent.root is None else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()
        
    
        # comments = Comment.objects.filter(content_type=comment.content_type,object_id=comment.object_id)
        

        # 返回数据
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.get_nickname_or_username()
        data['comment_time'] = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
        data['text'] = comment.text
        if not parent is None:
            data['reply_to'] = comment.reply_to.get_nickname_or_username()
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if not comment.root is None else ''
        # data['commens_nums'] = len(comments)
    else:
        #return render(request, 'error.html', {'message': comment_form.errors, 'redirect_to': referer})
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data)


def set_likes(request):
    data = {}
    # 获取数据
    ct = request.GET.get('ct')
    ct = ContentType.objects.get(model=ct)
    objid = int(request.GET.get('objid'))
    user = request.user

    # 存在就是要取消点赞，不存在就是进行点赞操作
    if Likes.objects.filter(content_type=ct,object_id=objid,usermakelike=user).exists():
        # 取消点赞
        # get出那条记录，删掉
        like = Likes.objects.get(content_type=ct,object_id=objid,usermakelike=user)
        like.delete()
        likes_count,created = Likes_count.objects.get_or_create(content_type=ct,object_id=objid)
        likes_count.like_count = likes_count.like_count - 1
        likes_count.save()
        data['active'] = ''
    else:
    # 点赞
        like = Likes(content_type=ct,object_id=objid,usermakelike=user)
        like.save()
        likes_count,created = Likes_count.objects.get_or_create(content_type=ct,object_id=objid)
        likes_count.like_count = likes_count.like_count + 1
        likes_count.save()
        data['active'] = 'active'

    data['status'] = 'SUCCESS'
    data['numbers'] = likes_count.like_count
    return JsonResponse(data)

'''def update_comment(request):
    referer = request.META.get('HTTP_REFERER', reverse('home'))

    # 数据检查
    if not request.user.is_authenticated:
        return render(request, 'error.html', {'message': '用户未登录', 'redirect_to': referer})
    text = request.POST.get('text', '').strip()
    if text == '':
        return render(request, 'error.html', {'message': '评论内容为空', 'redirect_to': referer})
    try:
        content_type = request.POST.get('content_type', '')
        object_id = int(request.POST.get('object_id', ''))
        model_class = ContentType.objects.get(model=content_type).model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except Exception as e:
        return render(request, 'error.html', {'message': '评论对象不存在', 'redirect_to': referer})
    
    # 检查通过，保存数据
    comment = Comment()
    comment.user = request.user
    comment.text = text
    comment.content_object = model_obj
    comment.save()
    return redirect(referer)'''