
from django import forms
from .models import User
from captcha.fields import CaptchaField


class UserForm(forms.Form):
    """
    用户名、密码、性别
    """
    name = forms.CharField(label='用户名', max_length=128,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(label='密码', max_length=256,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label="验证码")


class Register(forms.Form):
    gender = (
        ('male', '男'),
        ('female', '女'),
        ('other', '其他'),
    )
    name = forms.CharField(label='用户名', max_length=128,
                           widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(label='密码', max_length=256,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址",
                             widget=forms.EmailInput(attrs={'class': 'control'}))
    sex = forms.ChoiceField(label="性别", choices=gender)
    captcha = CaptchaField(label="验证码")


# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('name', 'password')
#         """
#         对用户表的名称进行命名==方法一：
#         """
#         labels = {
#             "name":"用户名",
#             "password":"密码"
#         }

    """
    对用户表的名称进行命名的==方法二：
    """
    # def __init__(self, *args, **kwargs):
    #     super(UserForm, self).__init__(*args, **kwargs)
    #     self.fields['name'].label = "用户名"
    #     self.fields['password'].label = "密码"
