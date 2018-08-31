from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import History, Bot
import aiml
import os

@login_required
def select_room(request):
    return render(request, 'chatbot/select_room.html')

@login_required
def frontdesk(request):
    return render(request, 'chatbot/frontdesk.html')

@login_required
def concierge(request):
    return render(request, 'chatbot/concierge.html')

@login_required
def activitiesdesk(request):
    return render(request, 'chatbot/activitiesdesk.html')

@login_required
def reservations(request):
    return render(request, 'chatbot/reservations.html')

@login_required
def frontdeskask(request):
    message = request.POST.get("messageText", "")
    kernel = aiml.Kernel()
    if os.path.isfile("bot_brain.brn"):
        kernel.bootstrap(brainFile = "bot_brain.brn")
    else:
        kernel.bootstrap(learnFiles = os.path.abspath("aiml/std-startup.xml"), commands = "load aiml b")
        kernel.saveBrain("bot_brain.brn")
    while True:
        bot_response = kernel.respond(message)
        instance = History.objects.create(user=request.user, bot=Bot.objects.get(name="frontdesk"), usertext=message, bottext=bot_response)
        return JsonResponse({'status':'OK','answer':bot_response})

