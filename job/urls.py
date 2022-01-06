from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter, DefaultRouter

app_name = 'job'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('api/', views.IndexApi.as_view(), name='indexapi'),
    path('detail/', views.DetailApi.as_view(), name='DetailApi'),
    path('GenericListApi/', views.GenericListApi.as_view(), name='GenericListApi'),
    path('GenericDetailApi/<str:pk>/', views.GenericDetailApi.as_view(), name='GenericDetailApi'),
    path('MixinListApi/', views.MixinListApi.as_view(), name='MixinListApi'),
    path('MixinDetailApi/<str:pk>/', views.MixinDetailApi.as_view(), name='MixinDetailApi'),
    path('ViewSetApi/', views.ViewSetApi.as_view({'get': 'list'})),
    path('ViewSetApi/<str:pk>/', views.ViewSetApi.as_view({'get': 'retrieve'})),
    path('ReadOnlyModelViewSetApi/', views.ReadOnlyModelViewSetApi.as_view({'get': 'list'})),
    path('ReadOnlyModelViewSetApi/<str:pk>/', views.ReadOnlyModelViewSetApi.as_view({'get': 'retrieve'})),
    # path('ModelViewSetApi/', views.ModelViewSetApi.as_view({'get': 'list', 'post': 'create'})),
    # path('ModelViewSetApi/change/<str:pk>/',
    #      views.ModelViewSetApi.as_view({'put': 'update_job_requires'})),
    # path('ModelViewSetApi/<str:pk>/',
    #      views.ModelViewSetApi.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

]
router = SimpleRouter()
router.register('job', views.ModelViewSetApi)  # 自动添加路由
urlpatterns += router.urls

print(urlpatterns)
