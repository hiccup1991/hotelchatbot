from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify

class CustomUser(AbstractUser):
    role = models.CharField(max_length=40)
    
    def __str__(self):
        return self.username

class ChatBotHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    usertext = models.TextField()
    bottext = models.TextField()
    chatdatetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.usertext + "&" + self.bottext

class Room(models.Model):
    name = models.CharField(max_length=40, unique=True)
    members = models.ManyToManyField(CustomUser, related_name="rooms")

    def __str__(self):
        return self.name

class Message(models.Model):
    room = models.ForeignKey(Room, related_name="messages")
    user = models.ForeignKey(CustomUser)

    content = models.CharField(max_length=250)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']