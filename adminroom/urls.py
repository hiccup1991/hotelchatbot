from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^admin/frontdesk/$', views.adminfrontdesk, name='adminfrontdesk'),
]