from django.db import models
from django.utils import timezone

class History(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    bot = models.ForeignKey('chatbot.Bot')
    usertext = models.TextField()
    bottext = models.TextField()
    chatdatetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.usertext + "&" + self.bottext

class Bot(models.Model):
    name = models.TextField()
    
    def __str__(self):
        return self.name
