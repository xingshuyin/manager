from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from job.views import ModelViewSetApi
from rest_framework.routers import DefaultRouter,SimpleRouter

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('index.urls')),
    path('graph/', include('graph.urls')),
    # path('manager/job/', include('job.urls'))
]
job_router = DefaultRouter()  # 创建router
job_router.register(prefix='job', viewset=ModelViewSetApi, basename='job')  # 注册view视图, prefix基本路径, viewset注册的视图, basename url的name的基本部分' basename+urlname
# 访问时根据  manager/job/-> list post , manager/job/pk  put delete get,  默认没有自定义方法
# 还可通过加  .json 返回json格式的数据

urlpatterns += job_router.urls  # 添加路由
print(urlpatterns)
