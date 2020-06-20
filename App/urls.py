from django.urls import path, include

from App import views
app_name='App'

urlpatterns = [
    #    path('admin/', admin.site.urls),
    path('index/',views.index,name='index'),

    path('category/<int:tid>/',views.category,name='category'),

    path('sale/<int:tid>/',views.sale,name='sale'),
    path('sale/',views.sale,name='sale'),

    path('details/',views.details,name='details'),
    path('details/<int:tid>/',views.details,name='details'),
    path('details/<int:tid>/<int:gid>/',views.details,name='details'),

    path('contact/',views.contact,name='contact'),

    path('handbags/<int:tid>/',views.handbags,name='handbags'),
    path('handbags/',views.handbags,name='handbags'),

    path('service/',views.service,name='service'),

    path('shoes/<int:tid>/', views.shoes, name='shoes'),
    path('shoes/',views.shoes,name='shoes'),

    path('wallents/<int:tid>/', views.wallents, name='wallents'),
    path('wallents/',views.wallents,name='wallents'),

    path('accessories/<int:tid>',views.accessories,name='accessories'),
    path('accessories/',views.accessories,name='accessories'),

    path('mans/<int:tid>/', views.mans, name='mans'),
    path('mans/<int:tid>/<int:page>/', views.mans, name='mans'),
    path('mans/', views.mans, name='mans'),

    path('news/<int:tid>/', views.news, name='news'),
    path('news/<int:tid>/<int:page>/', views.news, name='news'),
    path('news/', views.news, name='news'),

    path('logind/', views.loginb, name='login'),

    path('loginout/', views.loginout, name='loginout'),

    path('register/', views.register, name='register'),

    path('cart/', views.cart, name='cart'),
    path('cart/del/<int:gid>/', views.cart_del, name='cart_del'),

    path('palce_order/', views.palce_order, name='palce_order'),

    path('user_center_site/', views.user_center_site, name='user_center_site'),

    path('user_center_info/', views.user_center_info, name='user_center_info'),

    path('user_center_order/', views.user_center_order, name='user_center_order'),
    path('user_center_order/<int:page>/', views.user_center_order, name='user_center_order'),

    path('search/<str:keyword>/<int:page>/',views.search,name='serach'),

    path('add_goods/',views.add_goods,name='add_goods'),

# 文件上传
    path("upload/",views.upload,name='upload'),

]