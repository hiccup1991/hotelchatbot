from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from .forms import UserCreationForm
from .models import ChatAdminHistory, ChatBotHistory, CustomUser
import aiml
import os

import httplib
from urlparse import urlparse
import uuid, json


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
    output = json.dumps(json.loads(result), indent=4, ensure_ascii=False)
    output = json.loads(output)
    return output[0]['translations'][0]['text']

def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password = password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')
    return render(request, 'registration/login.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def select_room(request):
    return render(request, 'chatbot/select_room.html')

@login_required
def frontdesk(request):
    histories = ChatAdminHistory.objects.filter(chatdatetime__lte=timezone.now()).filter(user=request.user).filter(admin=CustomUser.get(role="frontdesk")).order_by('chatdatetime')
    return render(request, 'chatbot/frontdesk.html', {'histories': histories})
    # return render(request, 'chatbot/frontdesk.html')

@login_required
def concierge(request):
    histories = ChatAdminHistory.objects.filter(chatdatetime__lte=timezone.now()).filter(user=request.user).filter(admin=CustomUser.get(role="concierge")).order_by('chatdatetime')
    return render(request, 'chatbot/concierge.html', {'histories': histories})
    # return render(request, 'chatbot/concierge.html')

@login_required
def activitiesdesk(request):
    histories = ChatAdminHistory.objects.filter(chatdatetime__lte=timezone.now()).filter(user=request.user).filter(admin=CustomUser.get(role="activitiesdesk")).order_by('chatdatetime')
    return render(request, 'chatbot/activitiesdesk.html', {'histories': histories})
    # return render(request, 'chatbot/activitiesdesk.html')

@login_required
def operator(request):
    histories = ChatAdminHistory.objects.filter(chatdatetime__lte=timezone.now()).filter(user=request.user).filter(admin=CustomUser.get(role="operator")).order_by('chatdatetime')
    return render(request, 'chatbot/operator.html', {'histories': histories})
    # return render(request, 'chatbot/operator.html')

@login_required
def reservations(request):
    histories = ChatBotHistory.objects.filter(chatdatetime__lte=timezone.now()).filter(user=request.user).order_by('chatdatetime')
    return render(request, 'chatbot/reservations.html', {'histories': histories})
    # return render(request, 'chatbot/reservations.html')

@login_required
def frontdeskask(request):
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
    instance = History.objects.create(user=request.user, bot=Bot.objects.get(name="frontdesk"), usertext=message, bottext=bot_response)
    return JsonResponse({'status':'OK','answer':bot_response})

@login_required
def conciergeask(request):
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
    instance = History.objects.create(user=request.user, bot=ServiceAdmin.objects.get(name="concierge"), usertext=message, bottext=bot_response)
    return JsonResponse({'status':'OK','answer':bot_response})

@login_required
def activitiesdeskask(request):
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
    instance = History.objects.create(user=request.user, bot=ServiceAdmin.objects.get(name="activitiesdesk"), usertext=message, bottext=bot_response)
    return JsonResponse({'status':'OK','answer':bot_response})

@login_required
def operatorask(request):
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
    instance = History.objects.create(user=request.user, bot=ServiceAdmin.objects.get(name="operator"), usertext=message, bottext=bot_response)
    return JsonResponse({'status':'OK','answer':bot_response})

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