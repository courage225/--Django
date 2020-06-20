from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
# 用户表
class User(AbstractUser):
    uid = models.IntegerField(primary_key=True, auto_created=True)
    username = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=128)
    # 会员等级
    member_level = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.CharField(max_length=11)
    # 用户头像
    uimg = models.CharField(max_length=200)
    is_admin = models.BooleanField(default=True)
    class Meta:
        db_table = 'user'


# 地址表
class Address(models.Model):
    aid = models.IntegerField(primary_key=True, auto_created=True)
    uid = models.ForeignKey('User',on_delete=models.CASCADE, db_column='uid', blank=True, null=True)
    addre = models.CharField(max_length=200)
    # 是否是默认地址
    default_address = models.BooleanField()
    phone = models.CharField(max_length=11)
    receiver = models.CharField(max_length=20)
    class Meta:
        db_table = 'adderss'


# 订单信息表
class OrderInfo(models.Model):
    PAY_METHODS = {
        ('1', "货到付款"),
        ('2', "支付宝"),
    }
    ORDER_STATUS_CHOICES = (
        (1, '待支付'),
        (2, '待发货'),
        (3, '待评价'),
    )
    transit_choices = (
        (1, '申通快递'),
        (2, '圆通快递'),
        (3, '韵达快递'),
    )
    oid = models.IntegerField(primary_key=True, auto_created=True)
    uid = models.ForeignKey('User',  db_column='uid', on_delete=models.CASCADE)
    aid = models.ForeignKey('Address',  db_column='aid', on_delete=models.CASCADE)
    pay_mothod = models.SmallIntegerField(choices=PAY_METHODS, default=2)
    total_count = models.IntegerField(default=1)  # 商品数量
    total_price = models.IntegerField()  # 总价
    order_status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, default=1)  # 订单状态
    transit_price = models.SmallIntegerField(choices=transit_choices, default=1)  # 运费
    create_time = models.DateField()


    class Meta:
        db_table = 'order_info'


# 订单商品表
class OrdrGoods(models.Model):
    gid = models.IntegerField()
    oid = models.IntegerField(auto_created=True)
    goodnum = models.IntegerField()  # 数量
    goodprice = models.IntegerField()  # 价格
    uid = models.ForeignKey('User', db_column='uid', on_delete=models.CASCADE)
    class Meta:
        db_table = 'ordr_goods'


# 商品种类表
class GoodsType(models.Model):
    tid = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=20)
    type_num = models.IntegerField()

    class Meta:
        db_table = 'goods_type'


# 商品表
class Goods(models.Model):
    color_choices = (
        (0, '白色'),
        (1, '黑色'),
        (2, '灰色'),
        (3, '红色'),
    )
    status_choices = (
        (0, '无'),
        (1, '新品'),
        (2, '精品'),
        (3, '热销'),
    )
    gid = models.IntegerField(primary_key=True)
    tid = models.ForeignKey('GoodsType', on_delete=models.CASCADE, db_column='tid', blank=True, null=True)
    bid = models.ForeignKey('Brand', on_delete=models.CASCADE, db_column='bid', blank=True, null=True)
    gname = models.CharField(max_length=20)
    gtitle = models.CharField(max_length=200)  # 商品简介
    gdescription = models.CharField(max_length=200)  # 商品详情
    gprice = models.IntegerField()
    image = models.CharField(max_length=200)
    stock = models.IntegerField(default=1)  # 商品库存
    sales = models.IntegerField(default=0)  # 商品销量
    status = models.SmallIntegerField(default=0, choices=status_choices)  # '商品状态'
    gsize = models.CharField(max_length=10)
    gcolor = models.SmallIntegerField(choices=color_choices, default=0)
    is_del = models.BooleanField(default=True)



    class Meta:
        db_table = 'goods'

class Brand(models.Model):
    bid = models.IntegerField(primary_key=True)
    bname=models.CharField(max_length=20)
    bsotry = models.CharField(max_length=255)
    class Meta:
        db_table = 'brand'