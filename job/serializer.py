from rest_framework import serializers
import datetime
from .models import Jobs


class JobSerializer(serializers.Serializer):  # 创建序列化类
    def create(self, validated_data):  # 保存数据
        Jobs.objects.create(**validated_data)
        return 1

    def update(self, instance, validated_data):  # 更新数据
        print(instance.name)
        instance.name = 'kkk'
        for k, v in validated_data.items():
            print(k, v)
            if hasattr(instance, k):  # 判断是否有属性
                setattr(instance, k, v)  # 设置属性值
        instance.save()
        print(instance.name)
        # instance.update(**validated_data)
        return 1

    id = serializers.PrimaryKeyRelatedField(read_only=True)  # 选择想要展示的字段,字段名,字段类型和model的字段一样, 主键`外键
    name = serializers.CharField(max_length=128)
    company = serializers.CharField(max_length=200)
    salary = serializers.CharField(max_length=64)
    requires = serializers.CharField()
    issue = serializers.DateTimeField()
    education = serializers.CharField(max_length=64, allow_null=True, allow_blank=True)
    position = serializers.CharField(max_length=128, allow_null=True)
    platform = serializers.CharField(max_length=20)
    get_data = serializers.DateTimeField(default=datetime.datetime.now())
    # label_set = serializers.PrimaryKeyRelatedField(read_only=True, many=True)  # 关联他的的对象, 名字就是related_name的值
    label_set = serializers.StringRelatedField(read_only=True,
                                               many=True)  # 关联他的的对象的__str__(要有__str__方法), 名字就是related_name的值

    @staticmethod  # 用不着self或cls的话可以用静态方法
    def validate_name(value):  # 单字段校验
        if '?' in value:
            raise serializers.ValidationError("不能包含特殊符号")
        return value

    @staticmethod
    def validate(*args):  # 多字段校验, 直接用一个参数就行, 不用加*和索引访问
        # print(args[0])
        # print(args)
        if args[0]['issue'] > args[0]['get_data']:
            raise serializers.ValidationError("发布时间大于爬取时间")
        return args[0]
    # def validate(data):  # 多字段校验, 直接用一个参数就行, 不用加*和索引访问
    #     if data['issue'] > data['get_data']:
    #         raise serializers.ValidationError("发布时间大于爬取时间")
    #     return data


class JobModelSerializer(serializers.ModelSerializer):
    """
    内置了create,update方法
    """
    # input_psd = serializers.CharField(max_length=100)  # 添加额外的字段

    class Meta:
        model = Jobs  # 自动生成所有序列化字段
        fields = "__all__"  # all生成所有字段, ['name','issue','salary'] 列表或元组选择字段
        # read_only_fields = ['name']  # 设置只读字段, 修改无效
        # write_only_fields = ['company']
        extra_kwargs = {
            'name': {  # 修改字段参数
                'max_length': 200,
            },
            'position': {
                'max_length': 50
            },
            # 'company': {
            #     'write_only': True
            # }
        }

    # def validate(self, attrs):  # 字段验证
    #     if self.input_psd == attrs.get('psd'):
    #         return attrs
    #     else:
    #         raise serializers.ValidationError('密码错误')
