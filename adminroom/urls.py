from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^service/$', views.select_room, name='adminchatoom'),
    url(r'^service/livechatrooms/$', views.livechatrooms, name='livechatrooms'),
    url(r'^service/(?P<pk>\d+)/chatroom/$', views.selectedroom, name='selectedroom'),
    url(r'^service/(?P<pk>\d+)/sendmessage/$', views.sendmessage, name='sendmessage'),
    url(r'^service/(?P<pk>\d+)/messages/$', views.messages, name='messages'),
]