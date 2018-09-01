from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^service/$', views.select_room, name='admin_select_room'),
]