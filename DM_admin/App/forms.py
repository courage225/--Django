# 用户自定义表单
from django import  forms
from django.core.exceptions import ValidationError
import re

from django.forms.utils import ErrorList

from App.models import User


class ChangePwdForm(forms.Form):
    oldpwd = forms.CharField(min_length=8,required=True,error_messages={'required':'旧密码必填','min_length':'最短8位'})
    newpwd = forms.CharField(min_length=8,required=True,error_messages={'required':'新密码必填','min_length':'最短8位'})
    cfmpwd = forms.CharField(min_length=8,required=True,error_messages={'required':'确认密码必填','min_length':'最短8位'})

    # 单字段验证(新密码校验)
    def clean_newpwd(self):
        newpwd = self.cleaned_data.get('newpwd')
        check = re.match(r'^(?![A-Za-z]+$)(?![A-Z\\d]+$)(?![A-Z\\W]+$)(?![a-z\\d]+$)(?![a-z\\W]+$)(?![\\d\\W]+$)',
                         newpwd)
        if check:
            return newpwd
        else:
            raise ValidationError({'newpwd':"数字、字母、符号组合，最少8个字符"})

    # 全局验证(一致性校验)
    def clean(self):
        newpwd = self.cleaned_data.get('newpwd')
        cfmpwd = self.cleaned_data.get('cfmpwd')
        print(newpwd,cfmpwd)
        if newpwd != cfmpwd:
            raise ValidationError({'cfmpwd':"您所输入密码与新密码不一致，请重新输入！"})
        return self.cleaned_data



    # def clean_oldpwd(self):
    #     oldpwd = self.cleaned_data.get('oldpwd')
    #     username = self.cleaned_data.get('username')
    #     user = User.objects.filter(username=username, password=oldpwd)
    #     if user:
    #         return self.cleaned_data
    #     raise ValidationError( "用户名或密码错误，请重新输入！")


class RegisterForm(forms.Form):
    username = forms.CharField(min_length=3,required=True,error_messages={
        'required':'用户名必须输入',
        'min_length':'用户名至少3个字符'
    })
    password = forms.CharField(min_length=3,required=True,error_messages={
        'required': '密码名必须输入',
        'min_length': '密码至少3个字符'
    })
    confirm = forms.CharField(min_length=3,required=True,error_messages={
        'required': '密码名必须输入',
        'min_length': '密码至少3个字符'
    })
    regtime = forms.DateTimeField(required=False,error_messages={
        'invalid':'日期格式错误',
    })
    # 单个字段验证: clean_xxxx
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password and password.isdigit():
            raise ValidationError("密码不能是纯数字")
        return password

    def clean_username(self):
        username = self.cleaned_data.get('username')
        print(username)
        users = User.objects.filter(username=username).first()
        print(users)
        if username == users:
            raise ValidationError("用户已存在，请重新输入")
        return username
    # 全局验证
    def clean(self):
        password = self.cleaned_data.get('password',None)
        confirm = self.cleaned_data.get('confirm','')
        print(password,confirm)
        if password != confirm:
            raise ValidationError({'confirm':"两次密码输入不一致"})
        return self.cleaned_data

# 登录验证
class LoginForm(forms.Form):
    # def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
    #              initial=None, error_class=ErrorList, label_suffix=None,
    #              empty_permitted=False, field_order=None, use_required_attribute=None, renderer=None,request=None):
    #     super().__init__(data,files,auto_id,prefix,initial,error_class,label_suffix,empty_permitted,field_order,use_required_attribute,renderer,request)

    def clean(self):
        password = self.cleaned_data.get('password')
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username=username,password=password)
        print(password,username)
        print(user)
        if user:
            return self.cleaned_data
        raise ValidationError("用户名或密码错误，请重新输入！")
