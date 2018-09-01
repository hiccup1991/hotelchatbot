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
]