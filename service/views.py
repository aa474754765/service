from django.contrib.auth.models import User
from rest_framework import viewsets

from rest_framework.response import Response
from rest_framework import permissions, renderers, generics, status
from rest_framework.decorators import action
from service.permissions import IsOwnerOrReadOnly

from service.serializers import LogSerializer, RegisterSerializer, SnippetSerializer, UserSerializer
from service.models import Snippet


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    此视图自动提供`list`和`detail`操作。
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegisterView(generics.CreateAPIView):
    """
    此视图提供注册操作
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    # 注册不需要token
    permission_classes = []

    def create(self, request, *args, **kwargs):
        res = RegisterSerializer(data = request.data)
        if res.is_valid():
            res.save()
        return Response(res.errors)

class LogView(generics.CreateAPIView):
    """
    此视图提供登陆操作
    """
    queryset = User.objects.all()
    serializer_class = LogSerializer

    def create(self, request, *args, **kwargs):
        res = LogSerializer(data = request.data)
        if res.is_valid():
            return Response(res.validated_data)
        return Response(res.errors)


class SnippetViewSet(viewsets.ModelViewSet):
    """
    此视图自动提供`list`,`create`,`retrieve`,`update`和`destroy`操作。

    另外我们还提供了一个额外的`highlight`操作。
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly,)

    # @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# more simple case
# class SnippetList(generics.ListCreateAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer


# class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
