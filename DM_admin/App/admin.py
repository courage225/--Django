from django.contrib import admin

# Register your models here.
from App.models import User

# 用户管理
class UserAdmin(admin.ModelAdmin):
    # 显示哪些字段
    list_display = ['pk','username','password']
    #　搜索
    search_fields = ['username']
    # 分页
    list_per_page = 2
    # 过滤字段
    list_filter = ['username']
    #信息分组
    # fieldsets = [
    #     ('基本信息',{"fileds":['username']}),
    #     ('其他信息', {"fileds": ['password']}),
    # ]
    fieldsets = [
        ("基本信息", {"fields": ['username']}),
        ("其它信息", {'fields': ['password']}),
    ]

admin.site.register(User,UserAdmin)
