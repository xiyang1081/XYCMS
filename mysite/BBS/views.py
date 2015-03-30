#!/usr/bin/python
#coding=utf-8
import sys
reload(sys)
#sys.setdefaultencoding('utf-8')
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import HttpResponse,RequestContext
from django.shortcuts import HttpResponseRedirect
from BBS import models
from django.contrib.auth.models import User
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def Index(request):
    print request.user
    #if request.user.is_authenticated():
    #if request.COOKIES.get('username',''):
    if request.session.get('username',False) and request.COOKIES.get('username',''):
        username = request.session.get('username',False)
        print 'username:',username
        usernamecooks = request.COOKIES.get('username','')
        print 'cooks:',usernamecooks
        
        bbs_con=models.BbsContent.objects.all()
        return render_to_response('newbbs/index.html',{'bbs':bbs_con,'user':username})
    else:
        return HttpResponseRedirect('/login/')

@csrf_exempt
def Detail(request,bbs_id):
    if request.session.get('username',False) and request.COOKIES.get('username',''):
        username = request.session.get('username',False)
        print 'username:',username
        usernamecooks = request.COOKIES.get('username','')
        print 'cooks:',usernamecooks
        
        bbs_detail=models.BbsContent.objects.get(id=bbs_id)
        #print bbs_detail.author
        bbs_user=models.BbsUser.objects.get(user__username=bbs_detail.author)
        #头像路径修改
        bbs_user.image='/media/'+str(bbs_user.image)
        
        #回复列表
        answer=models.BbsUserAnswer.objects.filter(answer_bbs=bbs_id)
    
        
        if request.method=='POST' and request.POST.has_key('bbs_answer_Content') and request.POST['bbs_answer_Content'].strip()!='' and request.POST.has_key('bbs_answer_id'):
            #print 'post:',request.POST
            #print request.POST['bbs_answer_Content']
            answer_content=request.POST['bbs_answer_Content']
            answer_bbs=request.POST['bbs_answer_id']
            answer_datetime=datetime.datetime.now()
            answer_result=models.BbsUserAnswer.objects.create(answer_bbs=bbs_detail,answer_content=answer_content,answer_datetime=answer_datetime,answer_user=models.BbsUser.objects.get(user=User.objects.filter(username=username)))
            #print 'answer:',answer_result
            if answer:
                answer_result.save()
                return HttpResponseRedirect('/detail/%s/' %(bbs_detail.id))
                #return render_to_response('BBS/detail.html',{'detail':bbs_detail,'detail_head_img':bbs_user,'anw':answer})
            else:
                return HttpResponse(u"数据校验错误")
        
        return render_to_response('BBS/detail.html',{'detail':bbs_detail,'detail_head_img':bbs_user,'anw':answer,'user':username})
    else:
        return HttpResponseRedirect('/login/')

@csrf_exempt
def InsertContent(request):
    if request.session.get('username',False) and request.COOKIES.get('username',''):
        username = request.session.get('username',False)
        print 'username:',username
        usernamecooks = request.COOKIES.get('username','')
        print 'cooks:',usernamecooks
        
        category=models.Category.objects.all()
        
        if request.method=='POST':
            print request.POST
            title=request.POST['bbs_contitle']
            smarty=request.POST['bbs_consmarty']
            content=request.POST['bbs_content']
            select_category=request.POST['bbs_category']
            print title,smarty,content,select_category
                        
            insertcon=models.BbsContent.objects.create(title=title,
                                                       smarty=smarty,
                                                       contents=content,
                                                       category=models.Category.objects.get(category_name=select_category),
                                                       author=models.BbsUser.objects.get(user=User.objects.filter(username=username)),
                                                       )
            print insertcon
                #insertcon.save()
            return HttpResponseRedirect('/write/', {'user':username,'category':category})
        return render_to_response('BBS/insertcontent.html', {'user':username,'category':category})
    else:
        return HttpResponseRedirect('/login/')

@csrf_exempt
def Login(request):
    if request.method=='POST' and request.POST.has_key('username') and request.POST.has_key('password'):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['username'] = username
                response=HttpResponseRedirect('/')
                response.set_cookie('username',username,3600)
                #request.session
                # Redirect to a success page.
                return response
            else:
                return render(request,'BBS/login.html',{'error':"此用户未激活"})
        else:
            return render(request,'BBS/login.html',{'error':"此用户不存在"})
    return render(request,'BBS/login.html')

@login_required
def LoginOut(request):
    #print 'user:',request.user,request.session['username']
    del request.session['username']  #删除session
    response=HttpResponseRedirect('/login/')
    response.delete_cookie('username')
    #logout(request.user)
    return response