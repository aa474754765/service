from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from rest_framework import viewsets

from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response

from service.serializers import GroupSerializer, SnippetSerializer, UserSerializer
from service.models import Snippet

class UserViewSet(viewsets.ModelViewSet):
    """
    允许用户查看或编辑的 API 端点。
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    允许组查看或编辑的 API 端点。
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


# class JSONResponse(HttpResponse):
#     """
#     An HttpResponse that renders its content into JSON.
#     """
#     def __init__(self, data, **kwargs):
#         content = JSONRenderer().render(data)
#         kwargs['content_type'] = 'application/json'
#         super(JSONResponse, self).__init__(content, **kwargs)

@api_view(['GET', 'POST'])
def snippet_list(request, format=None):
    """
    列出所有的snippets，或者创建一个新的snippet。
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
    """
    获取，更新或删除一个snippet实例。
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)