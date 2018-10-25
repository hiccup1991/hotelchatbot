"""hotelchatbot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin


from chatbot import views as chatbotviews 

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/logout/$', chatbotviews.logout_user, name='logout'),
    url(r'^accounts/signup/$', chatbotviews.signup, name='signup'),
    url(r'^accounts/login/$', chatbotviews.login_user,  name='login'),
    url(r'', include('chatbot.urls')),
    url(r'', include('adminroom.urls')),
]
