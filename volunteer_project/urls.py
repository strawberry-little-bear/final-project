# volunteer_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  # 导入 Django 认证视图
from django.http import HttpResponseRedirect 
from django.urls import path
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('events/', include('events.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),  # 登录视图
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),  # 登出视图
       path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('', lambda request: HttpResponseRedirect('/events/')),  # 根路径重定向
]
