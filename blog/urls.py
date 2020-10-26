from django.urls import path

from . import views

urlpatterns = [
    # 设置了别名
    # 127.0.0.1:8000/blog/
    # start with blog
    path('',views.blog_list, name="blog_list"),
    path('<int:blog_pk>',views.blog_detail, name="blog_detail"),
    path('type/<int:blog_type_pk>',views.blogs_with_type,name="blogs_with_type"),
    # # re_path('^$',views.index),
    path('date/<int:year>/<int:month>',views.blogs_with_date,name="blogs_with_date"),

    ]