from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    # By default go to the login page
    url(r'^$', views.CodeList.as_view(), name='code-list'),
    url(r'^create/$', views.CodeCreate.as_view(), name='code-new'),
    url(r'^(?P<code_pk>\d+)/edit/$', views.CodeEdit.as_view(), name='code-edit'),
    url(r'^(?P<code_pk>\d+)/delete/$', views.CodeDelete.as_view(), name='code-delete'),
]
