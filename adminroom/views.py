from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login, logout, authenticate
from chatbot.models import ChatBotHistory, CustomUser, Message, Room

# encoding=utf8  
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

import aiml
import os

import httplib
from urlparse import urlparse
import uuid, json

import httplib
from urlparse import urlparse
import uuid, json

def reqtranslate(request):
    src = request.POST.get("src", "")
    tg = request.POST.get("tg", "")
    text = request.POST.get("text", "")
    if text != "" and tg != "":
        result = translate(text, "&from=" + src + "&to=" + tg)
        return JsonResponse({'status':'OK', 'result':result})

def translate (text, params):
    subscriptionKey = 'f6620d6414c24f40a96fab96b7ec9fe2'
    host = 'api.cognitive.microsofttranslator.com'
    path = '/translate?api-version=3.0'
    # params = "&to=es"
    # text = 'Hello, world!'

    requestBody = [{ 'Text' : text, }]
    content = json.dumps(requestBody, ensure_ascii=False).encode('utf-8')
    headers = {
        'Ocp-Apim-Subscription-Key': subscriptionKey,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    conn = httplib.HTTPSConnection(host)
    conn.request ("POST", path + params, content, headers)
    response = conn.getresponse ()
    result = response.read()
    output = json.dumps(json.loads(result), indent=4, ensure_ascii=False).encode('utf-8')
    output = json.loads(output)
    return output[0]['translations'][0]['text']

@login_required
def selectedroom(request, pk):
    instance = get_object_or_404(Room, pk=pk)
    messages = Message.objects.filter(room = instance)
    return render(request, 'chatroom.html', {'messages': messages, 'pk': instance.pk})

@login_required
def sendmessage(request, pk):
    if request.POST:
        message = request.POST.get("messageText", "")
        instance = get_object_or_404(Room, pk=pk)
        if message != "":
            instance = Message.objects.create(user=request.user, room = instance, content=message)
            return JsonResponse({'status':'OK'})
    else:
        return HttpResponse("request must be post")

@login_required
def select_room(request):
    rooms = Room.objects.filter(is_active = True).filter(name__contains=request.user.role)
    return render(request, 'select_room.html', {'livechatrooms': rooms})

@login_required
def livechatrooms(request):
    rooms = Room.objects.filter(is_active = True).filter(name__contains=request.user.role)
    customers = CustomUser.objects.filter(role="customer")
    return render(request, 'livechatrooms.html', {'livechatrooms': rooms, 'customers': customers})    

@login_required
def messages(request, pk):
    instance = get_object_or_404(Room, pk=pk)
    messages = Message.objects.filter(room = instance)
    return render(request, 'messages.html', {'messages': messages})

@login_required
def exitroom(request):
    return JsonResponse({'status':'OK'})

@login_required
def offerchat(request, customer):
    name = customer + request.user.role
    try:
        instance = Room.objects.get(name = name)
        instance.is_active = True
        instance.save()
    except:
        instance = Room.objects.create(name = name, is_active = True)
    return redirect('selectedroom', pk=instance.pk)

@login_required
def messageclear(request, pk):
    instance = get_object_or_404(Room, pk=pk)
    messages = Message.objects.filter(room = instance)
    messages.delete()
    return JsonResponse({'status':'OK'})
