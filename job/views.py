import rest_framework.authentication
from django.http import HttpResponse
from django.views.generic import ListView
from django.core.paginator import Paginator
from index.models import User, Token
from rest_framework import serializers
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from tools.tools import pages_divider
from .models import Jobs
from .serializer import JobModelSerializer


class Index(ListView):
    template_name = 'job/index.html'
    paginate_by = 10
    # ordering = 'issue'  # 排序列
    # job_serializer = JobSerializer(instance=Jobs.objects.all(), many=True)
    job_serializer = JobModelSerializer(instance=Jobs.objects.all(), many=True)  # 使用自动处理model的序列化器, many是否为多个对象

    model = Jobs

    # def get_queryset(self):
    #     return Jobs.objects.all()

    # def get(self, request, *args, **kwargs):  # 重写get参数
    #
    #     # print(self.job_serializer)
    #     return JsonResponse(self.job_serializer.data, safe=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['another'] = '其他的参数'
        context['page_range'] = pages_divider(context['page_obj'].number, context['paginator'].page_range)
        print(context)
        """
        {'paginator': None, 
        'page_obj': None, 
        'is_paginated': False, 
        'object_list': <QuerySet [<Jobs: Jobs object (00018e71bca90ceacb1bacde563bd236)>]>, 
        'jobs_list': <QuerySet [<Jobs: Jobs object (00018e71bca90ceacb1bacde563bd236)>]>, 
        'view': <job.views.Index object at 0x0000022DCD9883D0>, 
        'another': '其他的参数'}
        """
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST
        # d = JobSerializer(data=data)
        # if d.is_valid(raise_exception=True):
        #     # d.save()  # 保存反序列化的数据
        #     pass
        print(data['id'])
        d = JobModelSerializer(instance=Jobs.objects.get(id=data['id']), data=data)
        if d.is_valid(raise_exception=True):
            d.save()  # 更新反序列化的数据
            pass
        return HttpResponse('s')


# 一级视图
class IndexApi(APIView):  # 使用DRF的类视图
    def get(self, request):
        d = request.query_params  # 获取get参数
        page = request.query_params['page']

        return Response(data={'d': 1}, status=status.HTTP_200_OK)  # 使用DRF的响应,及状态码

    def post(self, request):
        d = request.data  # 获取表单参数
        return Response({'d': 1})


class DetailApi(APIView):
    def get(self, request):
        id_job = request.query_params['id']
        job = Jobs.objects.get(id=id_job)
        s_job = JobModelSerializer(instance=job, many=False)
        return Response(data=s_job.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data  # 可以用data也可以还用POST
        s = JobModelSerializer(data=data)
        print(data)
        if s.is_valid(raise_exception=True):
            s.save()
            return Response(data)
        raise serializers.ValidationError('error')

    def put(self, request):
        data = request.data
        job = Jobs.objects.get(id=data['id'])
        s = JobModelSerializer(instance=job, data=data)
        if s.is_valid(raise_exception=True):
            s.save()
            return Response(data)
        raise serializers.ValidationError('error')


# 二级视图>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 二级视图正好与django模板配合
# 三个属性三个方法 queryset,serializer_class,lookup_field及pagination_class(分页器)
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class Pager(PageNumberPagination):  # 创建自定义DRF分页器, 也可以在settings直接写全局分页配置, 继承GenericAPIView的类才能使用
    max_page_size = 10  # 每页最大显示数
    page_size = 5  # 默认每页数量
    page_query_param = 'page'  # 页码参数名
    page_size_query_param = 'page_size'  # 页码数据量参数名?page=5&page_size=8,  page_size可以不写使用page_size=5的值


class GenericListApi(GenericAPIView):  # 二级视图-列表
    template_name = 'job/index.html'
    model = Jobs
    queryset = model.objects.all().order_by('id')  # 通用数据集,必须用queryset
    serializer_class = JobModelSerializer  # 通用序列化器,必须用serializer_class

    class Pager(PageNumberPagination):  # 创建自定义DRF分页器, 也可以在settings直接写全局分页配置, 继承GenericAPIView的类才能使用
        max_page_size = 10  # 每页最大显示数
        page_size = 5  # 默认每页数量
        page_query_param = 'page'  # 页码参数名
        page_size_query_param = 'page_size'

    pagination_class = Pager

    def get(self, request):
        queryset = self.get_queryset()  # 获取数据用self.get_queryset()
        page = request.GET.get(self.pagination_class.page_query_param)
        page_range = pages_divider(page,
                                   range(round(self.model.objects.count() / self.pagination_class.page_size)))  # 占用过多时间
        paginate_queryset = self.paginate_queryset(self.filter_queryset(queryset))  # 二级视图获取分页后的数据
        serializer = self.get_serializer(instance=paginate_queryset,
                                         many=True)  # 获取序列化器用, self.get_serializer(instance=job,
        # many=True)
        # return Response(data=serializer.data, status=status.HTTP_200_OK)
        return render(request, self.template_name, {'data': paginate_queryset, 'page': page, 'page_range': page_range})

    def post(self, request):
        s = self.get_serializer(data=request.data)
        if s.is_valid():
            s.save()
        return HttpResponse('1')


class GenericDetailApi(GenericAPIView):  # 二级视图-详情
    queryset = Jobs.objects.all()  # 一般都是固定的 模型的all
    serializer_class = JobModelSerializer
    lookup_field = 'pk'  # 主键参数名(默认pk)

    # lookup_url_kwarg =

    def get(self, request, pk):
        job = self.get_object()  # 通过lookup_field, 从queryset中get想要的数据
        serializer = self.get_serializer(instance=job)  # 获取序列化器
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        job = self.get_object()
        serializer = self.get_serializer(instance=job, data=request.data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, pk):
        job = self.get_object()
        job.delete()
        return Response(data='success', status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


# 三级视图>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class MixinListApi(GenericAPIView, ListModelMixin, CreateModelMixin):  # Mixin, 通用的增删改查方法
    queryset = Jobs.objects.all()[:200]
    serializer_class = JobModelSerializer
    paginate_by = 2  # 分页数量 -> ListModelMixin
    page_kwarg = 'page'  # 页码参数  ->ListModelMixin

    def get(self, request):  # 获取
        return self.list(request)  # 这里的方法就是继承的ListModelMixin 创建的方法

    def post(self, request):  # 创建
        return self.create(request)


class MixinDetailApi(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):  #
    queryset = Jobs.objects.all()
    serializer_class = JobModelSerializer
    lookup_field = 'pk'  # 主键参数名(默认pk)

    lookup_url_kwarg = 'pk'

    def get(self, request, pk):
        a = self.retrieve(request)
        print(a)
        return self.retrieve(request)

    def put(self, request, pk):  # 修改
        return self.update(request)

    def delete(self, request, pk):  # 删除
        return self.destroy(request)


from rest_framework.viewsets import ViewSet, ModelViewSet, ReadOnlyModelViewSet
from django.shortcuts import get_object_or_404, render

# 视图集>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.
"""
ViewSet 路由映射  , path('api', viewset.as_view({'get':'list','post':'create'}),)
GenericViewSet  路由映射 三个属性三个方法 queryset,serializer_class,lookup_field
ModelViewSet 增删改查,三个属性三个方法
ReadOnlyModelViewSet  # 获取单个,获取列表
"""


# 视图集原理
class ViewSetApi(ViewSet):  # 提供了as_view的请求方式, 映射本身的方法(方法可以自定义)
    paginate_by = 10
    page_kwarg = 'page'  # 页码参数

    def list(self, request):
        queryset = Jobs.objects.all()
        p = Paginator(queryset, 10)
        serializer = JobModelSerializer(instance=p.page(request.query_params['page']), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        queryset = Jobs.objects.all()
        job = get_object_or_404(queryset, pk=pk)
        serializer = JobModelSerializer(instance=job)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 只读视图集
class ReadOnlyModelViewSetApi(ReadOnlyModelViewSet):  # 读取单个和列表,及请求映射
    queryset = Jobs.objects.all()
    serializer_class = JobModelSerializer
    lookup_field = 'pk'
    pagination_class = Pager  # 使用自定义分页器,请求时必须写page(page_query_param)和page_size(page_size_query_param)这两个参数, 继承GenericAPIView的类才能使用


from rest_framework.decorators import action
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class AuthClass(rest_framework.authentication.BasicAuthentication):  # 自定义身份验证
    def authenticate(self, request):
        if request.method == 'POST':
            token = request.POST.get('token')
            if t := Token.objects.get(token=token):
                return t.user, token


# 通用视图集
class ModelViewSetApi(ModelViewSet):  # 通用增删改查及请求方式映射
    queryset = Jobs.objects.all()
    serializer_class = JobModelSerializer
    lookup_field = 'pk'

    pagination_class = Pager  # 使用自定义分页器,请求时必须写page(page_query_param)和page_size(page_size_query_param)这两个参数, 继承GenericAPIView的类才能使用
    permission_class = [rest_framework.permissions.AllowAny]  # 局部权限验证
    authentication_classes = [IsAuthenticated]  # 局部身份验证
    throttle_classes = [AnonRateThrottle, UserRateThrottle]  # 局部限流
    throttle_scope = "my_throttle"  # 可选限流

    @action(methods=['put'], detail=True, url_path='change',
            url_name='change')  # 自动生成路由, methods允许访问的方式, url_path路径, basename(router中)+url_name = name(path中), detail是否需要传入lookup_field
    def update_job_requires(self, request, pk):  # 局部更新数据
        job = self.get_object()
        serializer = self.get_serializer(instance=job, data=request.data, partial=True)  # partial修改部分数据
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(request.data, status=status.HTTP_201_CREATED)
