#!/usr/bin/python
#coding=utf-8
from django.conf.urls import patterns, include, url
from BBS import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$',views.Index,name='index'),
    url(r'^detail/(\d+)/$',views.Detail,name='detail'),
    url(r'^login/$',views.Login,name='login'),
    url(r'^logout/$',views.LoginOut,name='logout'),
    url(r'^write/$',views.InsertContent,name='write'),
)
