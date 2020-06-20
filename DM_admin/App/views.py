import datetime
import os
import re
from random import randint
from time import time

from PIL import Image
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.http import request, HttpResponse, response
from django.shortcuts import render, redirect
from django.urls import reverse

from App.forms import RegisterForm, ChangePwdForm, LoginForm
# from App.models import Category, Article, User, Mark
from App.models import User, GoodsType, Goods, OrderInfo, Brand
from App.yzm import vc
from DM_admin import settings

# 装饰器，路由保护
def check_login(func):
    def inner(*args,**kwargs):
        print(args,kwargs)
        if args[0].COOKIES.get('username'):
            return func(*args,**kwargs)
        else:
            return redirect('/loginb/')
    return inner

@check_login
def index(request):
    return render(request, 'index.html')

# 左边导航栏
# @check_login
def public_left(request):
    return render(request, "public_left.html")


# @check_login
def public_header(request):
    # 获取用户ｓｅｓｓｉｏｎ信息
    # user = request.session.get('user')
    # print(user)
    username = request.session.get('username')
    # print(username)
    return render(request, 'public_header.html',locals())


# 商品管理
# @check_login
def public_main(request, cid=-1, page=1):
    categories = GoodsType.objects.all()
    # 获取所有分类id
    postion = [cat.tid for cat in categories]
    if request.method == "POST":
        cid = int(request.POST.get('cid', -1))
        keyword = request.POST.get('keyword', '')
        # 文章检索
        articles = Goods.objects.filter(tid=cid, gtitle__icontains=keyword)
    else:
        # 检索分类
        if cid < 0:
            first_category = categories.first() # 查询第一个分类
            cid = first_category.tid  # 第一个分类的cid
        # 文章检索
        articles = Goods.objects.filter(tid=cid)
    pos = postion.index(cid)
    # 分页
    paginator = Paginator(articles, 6)
    # 分页对象
    # page表示当前页面
    pager = paginator.page(page)
    return render(request, "wenzhang_xinwen.html", locals())

# 订单管理
def xitong_set(request,uid=-1,page=1):
    username = request.session.get('username')
    users = User.objects.exclude(username=username)
    postion = [cat.uid for cat in users]
    if request.method == "POST":
        mid = int(request.POST.get('cid', -1))
        keyword = request.POST.get('keyword', '')
        # 评论检索
        marks = OrderInfo.objects.filter(uid=uid)
    else:
        # 检索分类
        if uid < 0:
            first_mark = users.first()  # 查询第一个分类
            print(first_mark)
            uid = first_mark.uid  # 第一个分类的cid
        # 文章检索
        marks = OrderInfo.objects.filter(uid=661)
    pos = postion.index(uid)
    # 分页
    paginator = Paginator(marks, 6)
    # 分页对象
    pager = paginator.page(page)
    return render(request,'xitong_set.html',locals())



# 用户管理
def tupian_pc_index(request,uid=1,page=1):
    users = User.objects.all()
    # 获取所有分类id
    postion = [cat.uid for cat in users]
    if request.method == "POST":
        uid = int(request.POST.get('uid', -1))
        keyword = request.POST.get('keyword', '')
        # 用户检索
        users = User.objects.filter(username__icontains=keyword)
    pos = postion.index(uid)
    # 分页
    # paginator = BaiduPaginator(articles, 1)
    # pager = paginator.page(page)
    # pager.page_range = paginator.custom_range(page,2)
    paginator = Paginator(users, 4)
    # 分页对象
    # page表示当前页面
    pager = paginator.page(page)
    return render(request,"user.html",locals())


def public_super_cg(request):
    return render(request,'public_super_cg.html')

# 商品发布
# @check_login
def wenzhang_xinwen_fabu(request):
    categories = GoodsType.objects.all()
    print(categories[0].type_name)
    if request.method == "POST":
        mcid = request.POST.get('cid')
        cid = GoodsType.objects.filter(tid=mcid).first()
        a_cid = cid.tid
        title = request.POST.get('title')
        content = request.POST.get('content')
        create_time = request.POST.get('create_time')
        picture = request.session.get('photo')
        gprice = request.POST.get('gprice')
        bid = Brand.objects.first()
        # 添加商品
        Goods.objects.create(gid=randint(1000, 9999),
                             gname=title,
                             gtitle=title,
                             gdescription=content,
                             gprice=gprice,
                             image=picture,
                             status=1, stock=1, gcolor=1, gsize=1,
                             bid=bid,
                             tid=cid
                             )
        return render(request, "wenzhang_xinwen_fabu.html", locals())
        # return redirect(reverse("App:main2", kwargs={'cid':a_cid,'page':1}))
    return render(request,"wenzhang_xinwen_fabu.html",locals())


# 辅助工具，注册用户
# @check_login
def user_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data.pop("confirm")
            # 把用户写入数据库
            # 密码会做签名，不能手动签名加密password
            user = User.objects.create_user(**data)
            if user:
                print(user.uid)
                return redirect('/tupian_pc_index/')
            else:
                return render(request, "register.html", {'form': form})
        else:
            return render(request, "register.html", {'form': form})
        # get请求
    return render(request, "register.html")

# 修改密码
# @check_login
def change_psw(request):
    # 查询当前登录用户
    username = request.session.get('username')
    # 检查旧密码是否一致
    if request.method == 'POST':
        oldpwd = request.POST.get('oldpwd')
        newpwd = request.POST.get('newpwd')
        # print(oldpwd,newpwd)
        user = authenticate(username=username,password=oldpwd)
        # print(user)
        form = ChangePwdForm(request.POST)
        if user and form.is_valid():
            data = form.cleaned_data
            data.pop("cfmpwd")
            user.set_password(newpwd)
            user.save()
            return render(request,"loginb.html",locals())
        else:
            return render(request, "change_psw.html", {'form': form,"msg": u"用户名或者密码错误!"})
    # else:
    #     return render(request, "change_psw.html")
    return render(request,"change_psw.html",locals())


# 退出/登录
def loginb(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        code = request.POST.get('code')
        vcode = request.session.get('vcode')
        # print(code,vcode)
        user = authenticate(username=username, password=password)
        # print('1222')
        # print(user)
        # form = LoginForm(request.POST)
        # if form.is_valid():
        if user and (code == vcode):
            # print('sfddfsds')
             # 使用ｓｅｓｓｉｏｎ记录用户登录信息
            request.session['username'] = username
            login(request,user)
            # print(username)
            return render(request, "index.html", locals())
            # return redirect(reverse("App:main2", kwargs={'cid': 1, 'page': 1}))
    return render(request, "loginb.html",{"msg": u"用户名或者密码错误!"})

def user_loginout(request):
    logout(request)
    return redirect('/loginb/')

#　验证码
def get_verify_img(req):
    result = vc.generate()
    # 把验证码字符串保存到session
    req.session['vcode'] = vc.code
    # print('vcode')
    print(vc.code)
    # 将缓存区的内容返回给前端
    return HttpResponse(result,'image/png')


# 文件上传
# @check_login
def upload(request):
    if request.method == 'POST':
        #　获取文件上传的对象
        fobj = request.FILES.get('photo')
        path = os.path.join(settings.STATICFILES_DIRS[0],'upload')
        path = os.path.join(path,fobj.name)
        if fobj:
            # print(fobj.name,fobj.size)
            with  open(path,'wb') as target:
                # 文件大于２．５ｍ
                if fobj.multiple_chunks():
                   for data in fobj.chunks():
                       target.write(data)
                else:
                    target.write(fobj.read())
            request.session['photo'] = path.replace('/var/www/data/Tblog', '')#/home/courage/Tblog

            return HttpResponse('上传成功'+path)
    return render(request,'image.html')

#　删除文章
# @check_login
def del_article(request,aid,cid=-1,page=1):
    article = Goods.objects.filter(gid=aid)
    if article:
        article.delete()
    return redirect(reverse("App:main2", kwargs={'cid':cid, 'page':page}))

# 商品修改
# @check_login
def wenzhang_xinwen_xiugai(request,aid,cid=1):
    categories = GoodsType.objects.all()
    article = Goods.objects.filter(gid=aid).first()
    print(article.image)
    if article:
        if request.method == "POST":
            mcid = request.POST['cid']
            cid = GoodsType.objects.filter(cid=mcid).first()
            article.tid = cid
            article.gid = aid
            article.gprice = request.POST['gprice']
            article.gtitle = request.POST['title']
            article.gdescription = request.POST['content']
            article.image =request.session.get('photo')
            article.save()
    return render(request,'wenzhang_xinwen_xiugai.html', locals())

# 修改用户信息
# @check_login
def change_user(request,uid):
    # 查询当前登录用户
    username = request.session.get('username')
    user = User.objects.filter(uid=uid).first()
    # 检查旧密码是否一致
    if request.method == 'POST':
        oldpwd = request.POST.get('oldpwd')
        newpwd = request.POST.get('newpwd')
        # print(oldpwd,newpwd)
        user = authenticate(username=user.username, password=oldpwd)
        # print(user)
        form = ChangePwdForm(request.POST)
        if user and form.is_valid():
            data = form.cleaned_data
            data.pop("cfmpwd")
            user.set_password(newpwd)
            user.save()
            return render(request, "loginb.html", locals())
        else:
            return render(request, "change_user.html", {'form': form, "msg": u"用户名或者密码错误!"})
    # else:
    #     return render(request, "change_psw.html")
    return render(request, "change_user.html", locals())

# 删除用户
# @check_login
def del_user(request,uid):
    users = User.objects.filter(uid=uid)
    if users:
        users.delete()
    return redirect(reverse("App:tupian_pc_index"))

# 删除评论
# @check_login
def del_mark(request,mid,uid=1,page=1):
    mark = OrderInfo.objects.filter(mid=mid)
    print(mark)
    if mark:
        mark.delete()
    return redirect(reverse('App:xitong_set',kwargs={'uid':uid,'page':page}))

# 修改评论
# @check_login
def mark_xiugai(request,mid,uid,page=1):
    users = User.objects.all()
    mark = OrderInfo.objects.filter(mid=mid).first()
    # print(mark)
    # article = Article.objects.get(pk=aid)
    if mark:
        # print('ok')
        if request.method == "POST":
            mcid = request.POST['cid']
            uid = OrderInfo.objects.filter(uid=mcid).first()
            content = request.POST['content']
            content1 = content.replace('<p>','').replace('</p>','')
            mark.content=content1
            mark.save()
    return render(request, 'mark_xiugai.html', locals())

# 添加评论
# @check_login
def add_mark(request):
    users = User.objects.all()
    if request.method == "POST":
        mcid = request.POST['cid']
        uid = OrderInfo.objects.filter(uid=mcid).first()
        print(uid)
        print(uid.uid)
        content = request.POST['content']
        content1 = content.replace('<p>', '').replace('</p>', '')
        mark = OrderInfo.objects.create(mid=randint(100,999),content=content1,create_time=datetime.datetime.now().strftime('%Y-%m-%d'),uid=uid.uid)

    return render(request, 'mark_add.html', locals())