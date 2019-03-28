from django.conf.urls import url
from . import views

app_name = 'login'

urlpatterns = [
    url(r'^$',views.IndexView.as_view(), name='index'),
    url(r'login/$',views.LoginView.as_view(), name='login'),
    url(r'register/$', views.RegisterView.as_view(), name='register'),
    url(r'logout/$', views.LogoutView.as_view(), name='logout')
]
