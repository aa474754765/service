from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.forms import ValidationError
from rest_framework import serializers

from service.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class UserSerializer(serializers.ModelSerializer):

    snippets = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Snippet.objects.all())
    # owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = User
        fields = ('id', 'username', 'snippets')


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=16, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise ValidationError('两次密码输入不一致')
        del attrs['password2']
        attrs['password'] = make_password(attrs['password'])
        return super().validate(attrs)


class LogSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=6)

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, attrs):
        user_obj = User.objects.filter(username=attrs['username']).first()
        print(user_obj)
        if user_obj:
            if check_password(attrs['password'], user_obj.password):
                return super().validate('success')
        raise ValidationError('用户名或密码错误')


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style')

# class SnippetSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     code = serializers.CharField(style={'base_template': 'textarea.html'})
#     linenos = serializers.BooleanField(required=False)
#     language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
#     style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

#     def create(self, validated_data):
#         """
#         根据提供的验证过的数据创建并返回一个新的`Snippet`实例。
#         """
#         return Snippet.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         """
#         根据提供的验证过的数据更新和返回一个已经存在的`Snippet`实例。
#         """
#         instance.title = validated_data.get('title', instance.title)
#         instance.code = validated_data.get('code', instance.code)
#         instance.linenos = validated_data.get('linenos', instance.linenos)
#         instance.language = validated_data.get('language', instance.language)
#         instance.style = validated_data.get('style', instance.style)
#         instance.save()
#         return instance
