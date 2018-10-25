from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.select_room, name='select_room'),
    url(r'^frontdesk/$', views.frontdesk, name='frontdesk'),
    url(r'^concierge/$', views.concierge, name='concierge'),
    url(r'^activitiesdesk/$', views.activitiesdesk, name='activitiesdesk'),
    url(r'^operator/$', views.operator, name='operator'),
    url(r'^reservations/$', views.reservations, name='reservations'),
    url(r'^frontdeskask/$', views.frontdeskask, name='frontdeskask'),
    url(r'^conciergeask/$', views.conciergeask, name='conciergeask'),
    url(r'^activitiesdeskask/$', views.activitiesdeskask, name='activitiesdeskask'),
    url(r'^operatorask/$', views.operatorask, name='operatorask'),
    url(r'^reservationsask/$', views.reservationsask, name='reservationsask'),
    url(r'^frontdesk/messages/(?P<language>[-\w]+)/$', views.frontdeskmessages, name='frontdeskmessages'),
    url(r'^concierge/messages/(?P<language>[-\w]+)/$', views.conciergemessages, name='conciergemessages'),
    url(r'^operator/messages/(?P<language>[-\w]+)/$', views.operatormessages, name='operatormessages'),
    url(r'^activitiesdesk/messages/(?P<language>[-\w]+)/$', views.activitiesdeskmessages, name='activitiesdeskmessages'),
    url(r'^exitroom/(?P<roomtype>\w+)/$', views.exitroom, name='exitroom'),
    url(r'^frontdeskmessageclear/$', views.frontdeskmessageclear, name='frontdeskmessageclear'),
    url(r'^conciergemessageclear/$', views.conciergemessageclear, name='conciergemessageclear'),
    url(r'^activitiesdeskmessageclear/$', views.activitiesdeskmessageclear, name='activitiesdeskmessageclear'),
    url(r'^operatormessageclear/$', views.operatormessageclear, name='operatormessageclear'),
    url(r'^incomingchat/$', views.incomingchat, name='incomingchat'),
    url(r'^selectincomingchat/(?P<roomname>\w+)/$', views.selectincomingchat, name='selectincomingchat'),
    url(r'^translate/$', views.reqtranslate, name='reqtranslate'),
    url(r'^broadcastmessages/$', views.broadcastmessages, name='broadcastmessages'),
]