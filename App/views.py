import datetime
import os
import re
from random import random, randint

from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db.models import Count, Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.urls import reverse

from App.forms import RegisterForm
from App.models import Goods, GoodsType, Brand, User, OrdrGoods, OrderInfo, Address
from DM import settings


def index(request):
    sales = Goods.objects.filter(status=0, tid=7)
    curls = Goods.objects.filter(status=1, tid=7)
    tids = GoodsType.objects.filter(tid=7)
    mytid = tids[0].tid
    feature_goods1 = Goods.objects.filter(status=2,tid=5)[0:3]
    feature_goods2 = Goods.objects.filter(status=2,tid=5)[3:6]
    feature_goods = Goods.objects.filter(status=2,tid=5)
    good_types = GoodsType.objects.all()
    brands = Brand.objects.all()[0:6]
    mans = Goods.objects.filter(gname__icontains='男')[0:6]
    womans = Goods.objects.filter(gname__icontains='女')[0:6]
    username = request.session.get('username')
    if username:
        user = User.objects.filter(username=username).first()
        gprice = (OrdrGoods.objects.filter(uid=user.uid).aggregate(Sum('goodprice'))['goodprice__sum'])
        if gprice is None:
            gprice = 0
    else:
        gprice = 0
    if request.method == "POST":
        keyword = request.POST.get('keyword', '')
        return redirect(reverse("App:serach", kwargs={'keyword':keyword,'page':1}))
    return render(request,'index.html',locals())
    # return redirect(reverse("App:details", kwargs={'tid': mytid,'gid':mygid}))


def sale(request, tid):
    username = request.session.get('username')
    if username:
        user = User.objects.filter(username=username).first()
        gprice = (OrdrGoods.objects.filter(uid=user.uid).aggregate(Sum('goodprice'))['goodprice__sum'])
        if gprice is None:
            gprice = 0
    else:
        gprice = 0
    types = GoodsType.objects.all()
    good_type = GoodsType.objects.filter(tid=tid).first()
    good_types = GoodsType.objects.exclude(tid=tid)
    bags1 = Goods.objects.filter(tid=tid)[0:3]
    bags2 = Goods.objects.filter(tid=tid)[3:]
    feature_goods = Goods.objects.filter(tid=tid)[0:6]
    brands = Brand.objects.all()[0:6]
    mans = Goods.objects.filter(gname__icontains='男')[0:6]
    womans = Goods.objects.filter(gname__icontains='女')[0:6]
    sale_goods = Goods.objects.filter(tid=tid)
    # 获取所有分类id
    postion = [cat.tid for cat in types]
    if request.method == "POST":
        tid = int(request.POST.get('tid', -1))
        keyword = request.POST.get('keyword', '')
        # 文章检索
        sale_goods = Goods.objects.filter(tid=tid, gname__icontains=keyword)
        # print(sale_goods)
    else:
        # 检索分类
        if tid < 0:
            first_category = good_types.first()  # 查询第一个分类
            cid = first_category.cid  # 第一个分类的cid
        # 文章检索
        goods = Goods.objects.filter(tid=tid)
    pos = postion.index(tid)

    return render(request,'sale.html',locals())


def details(request, tid=1, gid=1):
    username = request.session.get('username')
    if username:
        user = User.objects.filter(username=username).first()
        cart_price = (OrdrGoods.objects.filter(uid=user.uid).aggregate(Sum('goodprice'))['goodprice__sum'])
        if cart_price is None:
            cart_price = 0
    else:
        cart_price = 0
    good_type = GoodsType.objects.filter(tid=tid).first()
    good_types = GoodsType.objects.exclude(tid=tid)
    bags1 = Goods.objects.filter(tid=tid)[0:3]
    bags2 = Goods.objects.filter(tid=tid)[3:]
    brands = Brand.objects.all()[0:6]
    brand = Brand.objects.all()
    feature_goods = Goods.objects.filter(status=2, tid=5)
    mans = Goods.objects.filter(gname__icontains='男')[0:6]
    womans = Goods.objects.filter(gname__icontains='女')[0:6]
    bests = Goods.objects.order_by('sales')[0:10]
    good = Goods.objects.get(gid=gid)
    bid = good.bid
    user_price = request.session.get('user_price')
    recode = []
    recode.append(user_price)
    count = len(recode)
    if request.method == "POST":
        keyword = request.POST.get('keyword')
        if keyword:
            return redirect(reverse("App:serach", kwargs={'keyword': keyword, 'page': 1}))
        tid = tid
        num = int(request.POST.get('num'))
        user_price = int(request.POST.get('user_price'))
        data_price = (Goods.objects.filter(gid=gid).first().gprice)
        cart_price += user_price * num
        address = Address.objects.filter(uid=661).first()
        order = OrdrGoods.objects.create(oid=randint(1000, 9999), goodnum=num, goodprice=user_price, gid=gid, uid=user)
        newg = Goods.objects.filter(gid=gid).update(gprice=user_price)
        request.session['user_price'] = user_price
        return render(request, 'details.html', locals())
    return render(request,'details.html', locals())


def contact(request):
    return render(request,'contact.html')


def handbags(request, tid):
    username = request.session.get('username')
    if username:
        user = User.objects.filter(username=username).first()
        gprice = (OrdrGoods.objects.filter(uid=user.uid).aggregate(Sum('goodprice'))['goodprice__sum'])
        if gprice is None:
            gprice = 0
    else:
        gprice = 0
    good_type = GoodsType.objects.filter(tid=tid).first()
    good_types = GoodsType.objects.exclude(tid=tid)
    bags1 = Goods.objects.filter(tid=tid)[0:3]
    bags2 = Goods.objects.filter(tid=tid)[3:]
    feature_goods = Goods.objects.filter(status=2, tid=5)
    brands = Brand.objects.all()[0:6]
    mans = Goods.objects.filter(gname__icontains='男')[0:6]
    womans = Goods.objects.filter(gname__icontains='女')[0:6]
    if request.method == "POST":
        keyword = request.POST.get('keyword', '')
        # feature_goods =  Goods.objects.filter(tid=tid).filter(gname__icontains=keyword)
        # print(feature_goods)
        return redirect(reverse("App:serach", kwargs={'keyword':keyword,'page':1}))
    return render(request,'handbags.html',locals())


def service(request):
    if request.method == "POST":
        keyword = request.POST.get('keyword', '')
        return redirect(reverse("App:serach", kwargs={'keyword': keyword, 'page': 1}))
    return render(request,'service.html')


def shoes(request, tid):
    username = request.session.get('username')
    if username:
        user = User.objects.filter(username=username).first()
        gprice = (OrdrGoods.objects.filter(uid=user.uid).aggregate(Sum('goodprice'))['goodprice__sum'])
        if gprice is None:
            gprice = 0
    else:
        gprice = 0
    good_type = GoodsType.objects.filter(tid=tid).first()
    good_types = GoodsType.objects.exclude(tid=tid)
    bags1 = Goods.objects.filter(tid=tid)[0:3]
    bags2 = Goods.objects.filter(tid=tid)[3:]
    feature_goods = Goods.objects.filter(tid=tid)
    brands = Brand.objects.all()[0:6]
    mans = Goods.objects.filter(gname__icontains='男')[0:6]
    womans = Goods.objects.filter(gname__icontains='女')[0:6]
    if request.method == "POST":
        keyword = request.POST.get('keyword', '')
        return redirect(reverse("App:serach", kwargs={'keyword': keyword, 'page': 1}))
    return render(request,'shoes.html',locals())


def wallents(request, tid):
    username = request.session.get('username')
    if username:
        user = User.objects.filter(username=username).first()
        gprice = (OrdrGoods.objects.filter(uid=user.uid).aggregate(Sum('goodprice'))['goodprice__sum'])
        if gprice is None:
            gprice = 0
    else:
        gprice = 0
    good_type = GoodsType.objects.filter(tid=tid).first()
    good_types = GoodsType.objects.exclude(tid=tid)
    bags1 = Goods.objects.filter(tid=tid)[0:3]
    bags2 = Goods.objects.filter(tid=tid)[3:]
    feature_goods = Goods.objects.filter(tid=tid)
    brands = Brand.objects.all()[0:6]
    mans = Goods.objects.filter(gname__icontains='男')[0:6]
    womans = Goods.objects.filter(gname__icontains='女')[0:6]
    if request.method == "POST":
        keyword = request.POST.get('keyword', '')
        # feature_goods =  Goods.objects.filter(tid=tid).filter(gname__icontains=keyword)
        # print(feature_goods)
        return redirect(reverse("App:serach", kwargs={'keyword':keyword,'page':1}))
    return render(request,'wallets.html',locals())


def accessories(request, tid):
    username = request.session.get('username')
    if username:
        user = User.objects.filter(username=username).first()
        gprice = (OrdrGoods.objects.filter(uid=user.uid).aggregate(Sum('goodprice'))['goodprice__sum'])
        if gprice is None:
            gprice = 0
    else:
        gprice = 0
    good_type = GoodsType.objects.filter(tid=tid).first()
    good_types = GoodsType.objects.exclude(tid=tid)
    bags1 = Goods.objects.filter(tid=tid)[0:3]
    bags2 = Goods.objects.filter(tid=tid)[3:]
    feature_goods = Goods.objects.filter(tid=tid)
    # 页脚数据
    brands = Brand.objects.all()[0:6]
    mans = Goods.objects.filter(gname__icontains='男')[0:6]
    womans = Goods.objects.filter(gname__icontains='女')[0:6]
    if request.method == "POST":
        keyword = request.POST.get('keyword', '')
        return redirect(reverse("App:serach", kwargs={'keyword': keyword, 'page': 1}))
    return render(request,'accessories.html',locals())


def category(request, tid):
    if tid == 1:
        return redirect(reverse("App:handbags", kwargs={'tid': 1}))
    elif tid == 2:
        return redirect(reverse("App:wallents", kwargs={'tid': 2}))
    elif tid == 3:
        return redirect(reverse("App:shoes", kwargs={'tid': 3}))
    elif tid == 4:
        return redirect(reverse("App:sale", kwargs={'tid': 4}))
    elif tid == 5:
        return redirect(reverse("App:accessories", kwargs={'tid': 5}))
    elif tid == 6:
        return redirect(reverse("App:mans", kwargs={'tid': 6}))
    elif tid == 7:
        return redirect(reverse("App:news", kwargs={'tid': 7,'page': 1}))


def mans(request, tid, page=1):
    username = request.session.get('username')
    if username:
        user = User.objects.filter(username=username).first()
        gprice = (OrdrGoods.objects.filter(uid=user.uid).aggregate(Sum('goodprice'))['goodprice__sum'])
        if gprice is None:
            gprice = 0
    else:
        gprice = 0
    good_type = GoodsType.objects.filter(tid=tid).first()
    good_types = GoodsType.objects.exclude(tid=tid)
    bags = Goods.objects.filter(gname__icontains='男')
    feature_goods = Goods.objects.filter(tid=5)
    brands = Brand.objects.all()[0:6]
    mans = Goods.objects.filter(gname__icontains='男')[0:6]
    womans = Goods.objects.filter(gname__icontains='女')[0:6]
    paginator = Paginator(bags,3)
    # 分页对象
    # page表示当前页面
    pager = paginator.page(page)
    if request.method == "POST":
        keyword = request.POST.get('keyword', '')
        # feature_goods =  Goods.objects.filter(tid=tid).filter(gname__icontains=keyword)
        # print(feature_goods)
        return redirect(reverse("App:serach", kwargs={'keyword': keyword, 'page': 1}))
    return render(request,'mans.html',locals())


def news(request,tid,page=1):
    username = request.session.get('username')
    if username:
        user = User.objects.filter(username=username).first()
        gprice = (OrdrGoods.objects.filter(uid=user.uid).aggregate(Sum('goodprice'))['goodprice__sum'])
        if gprice is None:
            gprice = 0
    else:
        gprice = 0
    good_type = GoodsType.objects.filter(tid=tid).first()
    good_types = GoodsType.objects.exclude(tid=tid)
    news = Goods.objects.filter(tid=7)
    # print(news)
    feature_goods = Goods.objects.filter(tid=tid)[0:6]
    brands = Brand.objects.all()[0:6]
    mans = Goods.objects.filter(gname__icontains='男')[0:6]
    womans = Goods.objects.filter(gname__icontains='女')[0:6]
    paginator = Paginator(news, 3)
    pager = paginator.page(page)
    if request.method == "POST":
        keyword = request.POST.get('keyword', '')
        # feature_goods =  Goods.objects.filter(tid=tid).filter(gname__icontains=keyword)
        # print(feature_goods)
        return redirect(reverse("App:serach", kwargs={'keyword': keyword, 'page': 1}))
    return render(request,'news.html',locals())


def search(request,keyword,page):
    username = request.session.get('username')
    if username:
        user = User.objects.filter(username=username).first()
        gprice = (OrdrGoods.objects.filter(uid=user.uid).aggregate(Sum('goodprice'))['goodprice__sum'])
        if gprice is None:
            gprice = 0
    else:
        gprice = 0
    feature_goods = Goods.objects.filter(tid=5)
    brands = Brand.objects.all()[0:6]
    mans = Goods.objects.filter(gname__icontains='男')[0:6]
    womans = Goods.objects.filter(gname__icontains='女')[0:6]
    bags = Goods.objects.filter(gname__icontains=keyword)
    paginator = Paginator(bags, 3)
    pager = paginator.page(page)
    if request.method == "POST":
        keyword = request.POST.get('keyword', '')
        # feature_goods =  Goods.objects.filter(tid=tid).filter(gname__icontains=keyword)
        # print(feature_goods)
        return redirect(reverse("App:serach", kwargs={'keyword': keyword, 'page': 1}))
    return render(request,'search.html',locals())


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # uid = randint(100,999)
            data = form.cleaned_data
            data.pop("confirm")
            data['uid'] = randint(100, 999)
            # 把用户写入数据库
            # 密码会做签名，不能手动签名加密password
            user = User.objects.create_user(**data)
            if user:
                print(user.uid)
                return redirect('/logind/')
            else:
                return render(request, "register.html", {'form': form})
        else:
            return render(request, "register.html", {'form': form})
        # get请求
    return render(request, "register.html")


def loginb(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(username=username, password=password)
        if user:
            # 使用ｓｅｓｓｉｏｎ记录用户登录信息
            request.session['username'] = username
            username = request.session.get('username')
            login(request, user)
            return redirect(reverse("App:index"))
    return render(request, "login.html", {"msg": u"用户名或者密码错误!"})


def cart(request):
    username = request.session.get('username')
    user = User.objects.filter(username=username).first()
    if request.method == "POST":
        keyword = request.POST.get('keyword', '')
        return redirect(reverse("App:serach", kwargs={'keyword': keyword, 'page': 1}))
    wating_pay_counts = OrdrGoods.objects.filter(uid=user.uid).aggregate(Count('oid'))['oid__count']
    wating_pay_goods = Goods.objects.raw('select * from ordr_goods where uid=661')
    return render(request, "cart.html", locals())


def palce_order(request):
    username = request.session.get('username')
    user = User.objects.filter(username=username).first()
    default_adds = Address.objects.filter(uid=user.uid, default_address=1).first()
    wating_pay_counts = OrdrGoods.objects.filter(uid=user.uid).aggregate(Count('oid'))['oid__count']
    wating_pay_goods = Goods.objects.raw('select * from ordr_goods where uid=661')
    gprice = (OrdrGoods.objects.filter(uid=user.uid).aggregate(Sum('goodprice'))['goodprice__sum'])
    if request.method == "POST":
        keyword = request.POST.get('keyword')
        if keyword:
            return redirect(reverse("App:serach", kwargs={'keyword': keyword, 'page': 1}))

        orderinfo = OrderInfo.objects.create(oid=randint(1000, 9999), uid=user, aid=default_adds,
                                             total_count=wating_pay_counts, total_price=gprice,
                                             create_time=datetime.datetime.now().strftime('%Y-%m-%d'))
        u1 = OrdrGoods.objects.filter(uid=user.uid)
        u1.delete()
        return redirect(reverse('App:index'))
    return render(request, "place_order.html", locals())


def user_center_site(request):
    username = request.session.get('username')
    user = User.objects.filter(username=username).first()
    default_adds = Address.objects.filter(uid=user.uid, default_address=1).first()
    if request.method == "POST":
        keyword = request.POST.get('keyword')
        if keyword:
            return redirect(reverse("App:serach", kwargs={'keyword': keyword, 'page': 1}))
        receiver = request.POST.get('receiver')
        addre = request.POST.get('addre')
        phone = request.POST.get('phone')
        # 校验数据
        if not all([receiver, addre, phone, type]):
            return render(request, 'user_center_site.html', {'errmsg': '数据不完整'})
        # 校验手机号
        if not re.match(r'^1[3|4|5|7|8][0-9]{9}$', phone):
            return render(request, 'user_center_site.html', {'errmsg': '手机格式不正确'})
        # 业务处理：地址添加
        # 如果用户已存在默认收货地址，添加的地址不作为默认收货地址，否则作为默认收货地址
        # 获取登录用户对应User对象
        user = request.user
        address = Address.objects.filter(uid=user.uid, default_address=1)
        if address:
            is_default = 0
        else:
            is_default = 1
        # 添加地址
        Address.objects.create(uid=user,
                               aid=randint(100,999),
                               receiver=receiver,
                               addre=addre,
                               phone=phone,
                               default_address=is_default)
    return render(request, "user_center_site.html",locals())


def user_center_info(request):
    username = request.session.get('username')
    user = User.objects.filter(username=username).first()
    default_adds =Address.objects.filter(uid=user.uid,default_address=1).first()
    if request.method == "POST":
        keyword = request.POST.get('keyword', '')
        return redirect(reverse("App:serach", kwargs={'keyword': keyword, 'page': 1}))
    return render(request,"user_center_info.html",locals())


def user_center_order(request, page=1):
    username = request.session.get('username')
    user = User.objects.filter(username=username).first()
    if request.method == "POST":
        keyword = request.POST.get('keyword')
        if keyword:
            return redirect(reverse("App:serach", kwargs={'keyword': keyword, 'page': 1}))

    orderinfo = OrderInfo.objects.filter(uid=user.uid)
    paginator = Paginator(orderinfo, 1)
    pager = paginator.page(page)
    return render(request,"user_center_order.html",locals())


def cart_del(request, gid=1):
    wating_pay_goods = Goods.objects.raw('select * from ordr_goods where uid=661')
    print(wating_pay_goods)
    return render(request, "cart.html", locals())


def loginout(request):
    logout(request)
    return redirect('/logind/')


def add_goods(request):
    goodtypes = GoodsType.objects.all()
    brands = Brand.objects.all()
    if request.method == "POST":
        mtid = request.POST.get('tid')
        tid = GoodsType.objects.filter(tid=mtid).first()
        mbid = request.POST.get('bid')
        bid = Brand.objects.filter(bid=mbid).first()
        gid = randint(1000, 9999)
        gname = request.POST.get('goodsname')
        gtitle = request.POST.get('goodstitle')
        image = request.session.get('photo')
        gprice = request.POST.get('goodsprice')
        status = request.POST.get('gstatus')
        stock = request.POST.get('gstock')
        gsize = request.POST.get('gsize')
        gcolor = request.POST.get('gcolor')
        gdescription = request.POST.get('gdescription')
        print(image,gprice,status,stock,gsize,gcolor, gdescription)
        # 添加商品
        Goods.objects.create(gid=gid,gname=gname,gtitle=gtitle,gdescription=gdescription,
                             gprice=gprice,image=image,status=status,stock=stock,gcolor=gcolor,gsize=gsize,
                             bid=bid,tid=tid
                             )
    return render(request,'product_detail.html',locals())



def upload(request):
    if request.method == 'POST':
    # 　获取文件上传的对象
        fobj = request.FILES.get('photo')
        path = os.path.join(settings.STATICFILES_DIRS[0], 'upload')
        path = os.path.join(path, fobj.name)
        if fobj:
            with open(path, 'wb') as target:
                # 文件大于２．５ｍ
                if fobj.multiple_chunks():
                    for data in fobj.chunks():
                        target.write(data)
                else:
                    target.write(fobj.read())
            request.session['photo'] = path.replace('/home/courage/PycharmProjects/DM', '')  # /home/courage/Tblog
            return HttpResponse('上传成功' + path)
    return render(request, 'image.html')