from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.hashers import make_password,check_password
from .models import User
from .form import UserForm,Register


# Create your views here.


class IndexView(View):
    def get(self,request):
        return render(request, 'login/index.html')


class LoginView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView,self).dispatch(request,*args,**kwargs)

    def get(self, request):
        login_form = UserForm()
        return render(request, 'login/login.html', {"userform": login_form})

    def post(self, request):

        msg = {
            "code": 1000,
            "msg": None
        }
        # username = request.POST.get("name")
        # password = request.POST.get("password")
        # captcha_num = request.POST.get('captcha_1')

        login_form = UserForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get("name")
            password = request.POST.get("password")

            if all([username, password]):
                try:
                    user = User.objects.filter(username=username).first()
                    db_pwd = user.password
                    check_password(password, db_pwd)
                except Exception as e:
                    msg['msg'] = "用户名或密码错误={}".format(e)
                    # return JsonResponse(msg)
                    return render(request, 'login/login.html', {'message': msg['msg']})
                # if username == user.username and check_password(password, user.password):
                #     print(username, password)
                #     return redirect('login:index')
                # msg['msg'] = "用户名或密码错误2"
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.username
                return redirect('login:index')

                # return JsonResponse(msg)
                # return render(request, 'login/login.html', {'message': msg['msg']})
            msg['msg'] = '用户名或密码不能为空'
            return render(request, 'login/login.html', {"message": msg['msg']})
        msg['msg'] = '验证码错误'
        return render(request, 'login/login.html', {'message': msg['msg']})


class RegisterView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(RegisterView,self).dispatch(request,*args,**kwargs)

    def get(self,request):
        if request.session.get('is_login', None):
            return redirect('login:index')
        register = Register()
        return render(request, 'login/register.html',locals())

    def post(self,request):
        msg = {
            "code": 1000,
            "msg": None
        }
        registr_form = Register(request.POST)
        if registr_form.is_valid():
            username = registr_form.cleaned_data['name']
            password = registr_form.cleaned_data['password']
            password2 = registr_form.cleaned_data['password2']
            email = registr_form.cleaned_data['email']
            sex = registr_form.cleaned_data['sex']
            if password != password2:
                msg['msg'] = "两次密码不一致"
                return render(request, 'login/register.html', {'message': msg['msg']})
            else:
                try:
                    user = User.objects.filter(username=username)
                except:
                    msg['msg'] = "用户名已存在"
                    return render(request, 'login/register.html', {'message': msg['msg']})
                # User.objects.create(registr_form)
                new_user = User()
                new_user.username = username
                new_user.password = make_password(password, None, 'pbkdf2_sha256')
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect('login:login')
        msg['msg'] = "验证码错误"
        return render(request,'login/register.html', {'message': msg['msg']})


class LogoutView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LogoutView,self).dispatch(request,*args,**kwargs)

    def get(self,request):
        """
        用户退出机制；
        删除session： request.session.flush()
        :param request:
        :return:
        """
        if not request.session.get('is_login',None):
            return redirect('login:index')
        request.session.flush()
        return redirect('login:index')


