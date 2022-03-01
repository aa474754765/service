from django.urls import re_path
from service import views

urlpatterns = [
    re_path(r'^snippets/$', views.snippet_list),
    re_path(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),
]