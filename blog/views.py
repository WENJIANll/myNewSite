from django.shortcuts import render,render_to_response,get_object_or_404
from .models import Blog,BlogType
from django.conf import settings
from django.core.paginator import Paginator
# Create your views here.

def get_blog_list_commoninfo(request,blogs_all_list):
    context = {}
    paginator = Paginator(blogs_all_list,settings.EACH_PAGE_BLOGS_NUMBER) # 每3页分一页
    page_num =  request.GET.get('page',1) # 获取页码参数（GET请求）
    page_of_blogs = paginator.get_page(page_num) #获取当前page页的数据
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

    context['page_range'] = page_range
    context['page_of_blogs'] = page_of_blogs
    context['blogs'] = page_of_blogs.object_list
    # context['blogs_count'] = Blog.objects.all().count()
    context['blog_types'] = BlogType.objects.all()
    context['blog_dates'] = Blog.objects.dates('created_time','month',order="DESC") 
    return context

def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_commoninfo(request,blogs_all_list)
    return render_to_response('blog/blog_list.html',context)

def blog_detail(request,blog_pk):
    context = {}
    blog = get_object_or_404(Blog,pk=blog_pk)
    context['previous_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).first()
    context['blog'] = blog
    return render_to_response('blog/blog_detail.html',context)

def blogs_with_type(request,blog_type_pk):
    blog_type = get_object_or_404(BlogType,pk=blog_type_pk)# 获取页面url传过来的分类
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_commoninfo(request,blogs_all_list)
    context['blog_type'] = blog_type  
    return render_to_response('blog/blogs_with_type.html',context)

def blogs_with_date(request,year,month):
    blogs_all_list = Blog.objects.filter(created_time__year=year,created_time__month=month)
    context = get_blog_list_commoninfo(request,blogs_all_list)
    context['blogs_with_date'] = '%s年%s月' % (year,month)
    return render_to_response('blog/blogs_with_date.html',context)
