# events/urls.py

from django.urls import path
from . import views
from django.urls import path
from .views import event_detail, join_event, cancel_participation
from .views import profile

urlpatterns = [
     path('register/', views.register, name='register'),
    path('', views.event_list, name='event_list'),  # 显示活动列表的路由
    path('create/', views.create_event, name='create_event'),  # 创建新活动
    path('<int:event_id>/', views.event_detail, name='event_detail'),  # 活动详情
    path('<int:event_id>/join/', views.join_event, name='join_event'),  # 加入活动
    path('events/cancel/<int:event_id>/', cancel_participation, name='cancel_participation'),
    path('profile/', profile, name='profile'),
  
]
