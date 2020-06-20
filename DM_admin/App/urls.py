from django.urls import path
from App import views
app_name = 'App'

urlpatterns = [
    path('', views.index, name='index'),
    # 左边导航栏
    path('left/',views.public_left, name='left'),

    # 右边的标题栏
    path('header/', views.public_header, name='header'),

    # 主窗口，内容展示
    path('main/',views.public_main, name='main'),
    path('main/<int:cid>/',views.public_main, name='main'),
    path('main/<int:cid>/<int:page>/',views.public_main, name='main2'),
    # 修改密码
    path("change_psw/", views.change_psw, name="change_psw.html"),
    # 修改用户信息
    path("change_user/<int:uid>", views.change_user, name="change_user.html"),
    # 登录
    path("loginb/", views.loginb, name='loginb.html'),
    # 退出
    path("login_out/", views.user_loginout, name='loginb.html'),

    # 用户管理页面
    path("tupian_pc_index/", views.tupian_pc_index, name="tupian_pc_index"),
    path("tupian_pc_index/<int:uid>/", views.tupian_pc_index, name="tupian_pc_index"),
    path("tupian_pc_index/<int:uid>/<int:page>", views.tupian_pc_index, name="tupian_pc_index"),

    # 评论设置页面
    path("xitong_set/", views.xitong_set, name='xitong_set'),
    path("xitong_set/<int:uid>/", views.xitong_set, name='xitong_set'),
    path("xitong_set/<int:uid>/<int:page>/", views.xitong_set, name='xitong_set'),

    path("public_super_cg/", views.public_super_cg, name='public_super_cg'),
    # 文章发布
    path("wenzhang_xinwen_fabu/", views.wenzhang_xinwen_fabu, name='wenzhang_xinwen_fabu'),
    # 添加评论
    path("add_mark/", views.add_mark, name='add_mark'),
    # 文章修改
    path("wenzhang_xinwen_xiugai/<int:aid>/<int:cid>/", views.wenzhang_xinwen_xiugai, name='wenzhang_xinwen_xiugai'),
    # 评论修改
    path("mark_xiugai/<int:mid>/<int:uid>/", views.mark_xiugai, name='mark_xiugai'),
    # 验证码
    path("get_verify_img",views.get_verify_img,name='get_verify_img'),

    #　注册用户
    path("user_register",views.user_register,name='user_register'),

    # 文件上传
    path("upload/",views.upload,name='upload'),

    # 文件删除
    path("delete/<int:aid>/<int:cid>/<int:page>/",views.del_article,name='del_article'),
    # 用户删除
    path("delete/<int:uid>/",views.del_user,name='del_user'),
    # 评论删除
    path("del_mark/<int:mid>/<int:uid>/<int:page>/", views.del_mark, name='del_mark'),

]
