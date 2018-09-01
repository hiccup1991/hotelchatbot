from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

from .models import History, ServiceAdmin
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

def adminfrontdesk(request):
    histories = History.objects.filter(chatdatetime__lte=timezone.now()).filter(user=request.user).filter(bot=Bot.objects.get(name="frontdesk")).order_by('chatdatetime')
    return render(request, 'chatbot/frontdesk.html', {'histories': histories})
    # return render(request, 'chatbot/frontdesk.html')

def adminfrontdeskask(request):
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
