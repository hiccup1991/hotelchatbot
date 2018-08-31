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
    histories = History.objects.filter(chatdatetime__lte=timezone.now()).filter(user=request.user).filter(bot=Bot.objects.get(name="frontdesk")).order_by('chatdatetime')
    return render(request, 'chatbot/frontdesk.html', {'histories': histories})
    # return render(request, 'chatbot/frontdesk.html')

@login_required
def concierge(request):
    histories = History.objects.filter(chatdatetime__lte=timezone.now()).filter(user=request.user).filter(bot=Bot.objects.get(name="concierge")).order_by('chatdatetime')
    return render(request, 'chatbot/concierge.html', {'histories': histories})
    # return render(request, 'chatbot/concierge.html')

@login_required
def activitiesdesk(request):
    histories = History.objects.filter(chatdatetime__lte=timezone.now()).filter(user=request.user).filter(bot=Bot.objects.get(name="activitiesdesk")).order_by('chatdatetime')
    return render(request, 'chatbot/activitiesdesk.html', {'histories': histories})
    # return render(request, 'chatbot/activitiesdesk.html')

@login_required
def reservations(request):
    histories = History.objects.filter(chatdatetime__lte=timezone.now()).filter(user=request.user).filter(bot=Bot.objects.get(name="reservations")).order_by('chatdatetime')
    return render(request, 'chatbot/reservations.html', {'histories': histories})
    # return render(request, 'chatbot/reservations.html')

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

@login_required
def conciergeask(request):
    message = request.POST.get("messageText", "")
    kernel = aiml.Kernel()
    if os.path.isfile("bot_brain.brn"):
        kernel.bootstrap(brainFile = "bot_brain.brn")
    else:
        kernel.bootstrap(learnFiles = os.path.abspath("aiml/std-startup.xml"), commands = "load aiml b")
        kernel.saveBrain("bot_brain.brn")
    while True:
        bot_response = kernel.respond(message)
        instance = History.objects.create(user=request.user, bot=Bot.objects.get(name="concierge"), usertext=message, bottext=bot_response)
        return JsonResponse({'status':'OK','answer':bot_response})

@login_required
def activitiesdeskask(request):
    message = request.POST.get("messageText", "")
    kernel = aiml.Kernel()
    if os.path.isfile("bot_brain.brn"):
        kernel.bootstrap(brainFile = "bot_brain.brn")
    else:
        kernel.bootstrap(learnFiles = os.path.abspath("aiml/std-startup.xml"), commands = "load aiml b")
        kernel.saveBrain("bot_brain.brn")
    while True:
        bot_response = kernel.respond(message)
        instance = History.objects.create(user=request.user, bot=Bot.objects.get(name="activitiesdesk"), usertext=message, bottext=bot_response)
        return JsonResponse({'status':'OK','answer':bot_response})

@login_required
def reservationskask(request):
    message = request.POST.get("messageText", "")
    kernel = aiml.Kernel()
    if os.path.isfile("bot_brain.brn"):
        kernel.bootstrap(brainFile = "bot_brain.brn")
    else:
        kernel.bootstrap(learnFiles = os.path.abspath("aiml/std-startup.xml"), commands = "load aiml b")
        kernel.saveBrain("bot_brain.brn")
    while True:
        bot_response = kernel.respond(message)
        instance = History.objects.create(user=request.user, bot=Bot.objects.get(name="reservations"), usertext=message, bottext=bot_response)
        return JsonResponse({'status':'OK','answer':bot_response})