from django.urls import path
from . import views
# 本地路由代码
urlpatterns=[
    # path('',views.msgproc),#留言相关功能
    path('operate/',views.operate),#操作相关功能
    path('index/',views.index),#response相关功能
]