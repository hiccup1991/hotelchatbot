from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login, logout, authenticate
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import ChatBotHistory, CustomUser, Message, Room

# encoding=utf8  
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

import aiml
import os

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
    print(output)
    output = json.loads(output)
    return output[0]['translations'][0]['text']

def login_user(request):
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if user.role == "customer":
                    return redirect('/')
                else:
                    return redirect('/service/')
    return render(request, 'registration/login.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = raw_password)
            login(request, user)
            if user.role == "customer":
                return redirect('/')
            else:
                return redirect('/service/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def select_room(request):
    return render(request, 'chatbot/select_room.html')

@login_required
def frontdesk(request):
    name = request.user.username + "frontdesk"
    try:
        instance = Room.objects.get(name = name)
        instance.is_active = True
        instance.save()
    except:
        instance = Room.objects.create(name = name, is_active = True)
    return render(request, 'chatbot/frontdesk.html')

@login_required
def concierge(request):
    name = request.user.username + "concierge"
    try:
        instance = Room.objects.get(name = name)
        instance.is_active = True
        instance.save()
    except:
        instance = Room.objects.create(name = name, is_active = True)
    return render(request, 'chatbot/concierge.html')


@login_required
def activitiesdesk(request):
    name = request.user.username + "activitiesdesk"
    try:
        instance = Room.objects.get(name = name)
        instance.is_active = True
        instance.save()
    except:
        instance = Room.objects.create(name = name, is_active = True)
    return render(request, 'chatbot/activitiesdesk.html')

@login_required
def operator(request):
    name = request.user.username + "operator"
    try:
        instance = Room.objects.get(name = name)
        instance.is_active = True
        instance.save()
    except:
        instance = Room.objects.create(name = name, is_active = True)
    return render(request, 'chatbot/operator.html')

@login_required
def reservations(request):
    histories = ChatBotHistory.objects.filter(chatdatetime__lte=timezone.now()).filter(user=request.user).order_by('chatdatetime')
    instances = []
    if histories.count() > 0:
        instance = ChatBotHistory.objects.create(user = request.user, usertext = "", bottext = "Hi, " + request.user.username + ", Nice to meet you again.")
    else:
        instance = ChatBotHistory.objects.create(user = request.user, usertext = "", bottext = "Hi, " + request.user.username)
    instances.append(instance)
    # return render(request, 'chatbot/reservations.html', {'histories': histories})
    return render(request, 'chatbot/reservations.html', {'histories': instances})

@login_required
def frontdeskask(request):
    if request.POST:
        message = request.POST.get("messageText", "")
        roomname = request.user.username + "frontdesk"
        if message != "" and roomname != "":
            instance = Message.objects.create(user=request.user, room = Room.objects.get(name=roomname), content=message)
            return JsonResponse({'status':'OK'})
    else:
        return HttpResponse("request must be post")

@login_required
def conciergeask(request):
    if request.POST:
        message = request.POST.get("messageText", "")
        roomname = request.user.username + "concierge"
        if message != "" and roomname != "":
            instance = Message.objects.create(user=request.user, room = Room.objects.get(name = roomname), content=message)
            return JsonResponse({'status':'OK'})
    else:
        return HttpResponse("request must be post")

@login_required
def activitiesdeskask(request):
    if request.POST:
        message = request.POST.get("messageText", "")
        roomname = request.user.username + "activitiesdesk"
        if message != "" and roomname != "":
            instance = Message.objects.create(user=request.user, room = Room.objects.get(name = roomname), content=message)
            return JsonResponse({'status':'OK'})
    else:
        return HttpResponse("request must be post")

@login_required
def operatorask(request):
    if request.POST:
        message = request.POST.get("messageText", "")
        roomname = request.user.username + "operator"
        if message != "" and roomname != "":
            instance = Message.objects.create(user=request.user, room = Room.objects.get(name = roomname), content=message)
            return JsonResponse({'status':'OK'})
    else:
        return HttpResponse("request must be post")

@login_required
def reservationsask(request):
    message = request.POST.get("messageText", "")
    language = request.POST.get("language", "")
    englishmessage = message
    if language != "en":
        englishmessage = translate(message, "&to=en")
    kernel = aiml.Kernel()
    if os.path.isfile("bot_brain.brn"):
        kernel.bootstrap(brainFile = "bot_brain.brn")
    else:
        kernel.bootstrap(learnFiles = os.path.abspath("aiml/std-startup.xml"), commands = "load aiml b")
        kernel.saveBrain("bot_brain.brn")

    bot_response = kernel.respond(englishmessage)
    if language != "en":
        bot_response = translate(bot_response, "&to="+language)
    instance = ChatBotHistory.objects.create(user=request.user, usertext=message, bottext=bot_response)
    return JsonResponse({'status':'OK','answer':bot_response})

@login_required
def frontdeskmessages(request):
    roomname = request.user.username + "frontdesk"
    instance = Room.objects.get(name = roomname)
    messages = Message.objects.filter(room = instance)
    return render(request, 'chatbot/messages.html', {'messages': messages})

@login_required
def conciergemessages(request):
    roomname = request.user.username + "concierge"
    instance = Room.objects.get(name = roomname)
    messages = Message.objects.filter(room = instance)
    return render(request, 'chatbot/messages.html', {'messages': messages})

@login_required
def activitiesdeskmessages(request):
    roomname = request.user.username + "activitiesdesk"
    instance = Room.objects.get(name = roomname)
    messages = Message.objects.filter(room = instance)
    return render(request, 'chatbot/messages.html', {'messages': messages})

@login_required
def operatormessages(request):
    roomname = request.user.username + "operator"
    instance = Room.objects.get(name = roomname)
    messages = Message.objects.filter(room = instance)
    return render(request, 'chatbot/messages.html', {'messages': messages})

@login_required
def exitroom(request, roomtype):
    if(roomtype != ""):
        roomname = request.user.username + roomtype
        instance = Room.objects.get(name = roomname)
        instance.is_active = False
        instance.save()
    return redirect('/')

@login_required
def frontdeskmessageclear(request):
    roomname = request.user.username + "frontdesk"
    instance = Room.objects.get(name = roomname)
    Message.objects.filter(room = instance).delete()
    return JsonResponse({'status':'OK'})

@login_required
def operatormessageclear(request):
    roomname = request.user.username + "operator"
    instance = Room.objects.get(name = roomname)
    Message.objects.filter(room = instance).delete()
    return JsonResponse({'status':'OK'})


@login_required
def conciergemessageclear(request):
    roomname = request.user.username + "concierge"
    instance = Room.objects.get(name = roomname)
    Message.objects.filter(room = instance).delete()
    return JsonResponse({'status':'OK'})


@login_required
def activitiesdeskmessageclear(request):
    roomname = request.user.username + "activitiesdesk"
    instance = Room.objects.get(name = roomname)
    Message.objects.filter(room = instance).delete()
    return JsonResponse({'status':'OK'})

@login_required
def incomingchat(request):
    incomingchats = Room.objects.filter(name__startswith=request.user.username).filter(is_active = True)
    return render(request, 'chatbot/incomingchat.html', {'incomingchats': incomingchats})    

@login_required
def selectincomingchat(request, roomname):
    if roomname.endswith("frontdesk"):
        return redirect('frontdesk')   
    if roomname.endswith("concierge"):
        return redirect('concierge')   
    if roomname.endswith("activitiesdesk"):
        return redirect('activitiesdesk')   
    if roomname.endswith("operator"):
        return redirect('operator')    