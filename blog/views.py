import markdown
from django.shortcuts import render,get_object_or_404
from django.conf import settings
from django.db.models import Count
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType

from read_account.models import ReadNum
from .models import Blog,BlogType
from read_account.utils import read_account_once
from comment.models import Comment ,Likes,Likes_count
from comment.forms import CommentForm

# Create your views here.

def get_blog_list_commoninfo(request,blogs_all_list):
    context = {}
    paginator = Paginator(blogs_all_list,settings.EACH_PAGE_BLOGS_NUMBER) # 每3页分一页
    page_num =  request.GET.get('page',1) # 获取页码参数（GET请求）
    page_of_blogs = paginator.get_page(page_num) #获取当前page页的数据，getpage这个方法已经把page_num是不是整形考虑倒了
    curent_page_num = page_of_blogs.number
    # 列表生成器生成左右的共五个页码
    page_range = [i for i in range(curent_page_num-2, curent_page_num+3) if i > 0 and (i <= paginator.num_pages)] 
    # 加上省略号 这里的2就是上面列表生成器上的2
    if page_range[0] -1 >= 2:
        page_range.insert(0,'...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首和尾
    if page_range[0] != 1:
        page_range.insert(0,1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    # 获取博客的分类和对应的数量
    # 下面的blog_blog是models里面写的
    blog_type_list = BlogType.objects.annotate(blog_count = Count('blog_blog'))
    # 下面的语句会造成服务器的负担，这是在内存中处理
    '''blog_types = BlogType.objects.all()
    blog_type_list = []
    for blog_type in blog_types:
        blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
        blog_type_list.append(blog_type)
    '''
    # 获取日期对应的博客数量
    # dates()这个方法，第一个参数是字段，第二个是类型，第三个是按什么顺序
    # retrun一个queryset
    blog_dates = Blog.objects.dates('created_time','month',order="DESC") 
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                         created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count
    context['page_range'] = page_range
    context['page_of_blogs'] = page_of_blogs
    context['blogs'] = page_of_blogs.object_list
    # context['blogs_count'] = Blog.objects.all().count()
    context['blog_types'] = blog_type_list
    context['blog_dates'] = blog_dates_dict
    context['page_currn_num'] = page_num
    return context

def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_commoninfo(request,blogs_all_list)

    return render(request,'blog/blog_list.html',context)

def blog_detail(request,blog_pk):
    context = {}
    blog = get_object_or_404(Blog,pk=blog_pk)
    read_cookie_key = read_account_once(request,blog)
        # log.readed_num += 1
        # blog.save()'''
    blog_content_type = ContentType.objects.get_for_model(blog)
    # 这个使用模板标签get_comment_list实现了
    # comments = Comment.objects.filter(content_type=blog_content_type,object_id=blog.pk,parent=None)

    if Likes_count.objects.filter(content_type=blog_content_type,object_id=blog_pk):
        likecount = Likes_count.objects.get(content_type=blog_content_type,object_id=blog_pk)
        likesnum = likecount.like_count
    else:
        likesnum = 0
    blogs_all_list = Blog.objects.filter(blog_type=blog.blog_type)
    context = get_blog_list_commoninfo(request,blogs_all_list)
    context['previous_blog'] = Blog.objects.filter(created_time__lt=blog.created_time,blog_type=blog.blog_type).last()
    context['next_blog'] = Blog.objects.filter(created_time__gt=blog.created_time,blog_type=blog.blog_type).first()
    context['blog'] = blog  
    context['blog_content'] = markdown.markdown(blog.content,
                                  extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                  ])
    context['likesnum'] = likesnum
    # context['comments'] = comments
    # 这个使用模板标签get_comment_form实现了
    # context['comment_form'] = CommentForm(initial={'content_type': blog_content_type.model, 'object_id': blog_pk,'reply_comment_id':0})

    # context['user'] = request.user
    response = render(request,'blog/blog_detail.html',context)
    # print(context['comments'])
    response.set_cookie(read_cookie_key,'Ture',max_age=21600) # cookie类似字典的东西
    return response

def blogs_with_type(request,blog_type_pk):
    blog_type = get_object_or_404(BlogType,pk=blog_type_pk)# 获取s
    # 页面url传过来的分类
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    # context = get_blog_list_commoninfo(request,blogs_all_list)
    context = {}
    context = get_blog_list_commoninfo(request,blogs_all_list)
    context['blog_type'] = blog_type  
    context['blog_type_desc'] = markdown.markdown(blog_type.desc,
                                  extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                  ])
    return render(request,'blog/blogs_with_type.html',context)

def blogs_with_date(request,year,month):
    blogs_all_list = Blog.objects.filter(created_time__year=year,created_time__month=month)
    context = get_blog_list_commoninfo(request,blogs_all_list)
    context['blogs_with_date'] = '%s年%s月' % (year,month)
    return render(request,'blog/blogs_with_date.html',context)
