from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    role = models.TextField(1)
    
    def __str__(self):
        return self.username

class ChatBotHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    usertext = models.TextField()
    bottext = models.TextField()
    chatdatetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.usertext + "&" + self.bottext

class ChatAdminHistory(models.Model):
    user = models.ForeignKey(CustomUser, related_name = "customer", on_delete=models.CASCADE)
    admin = models.ForeignKey(CustomUser, related_name = "seviceadmin", on_delete=models.CASCADE)
    usertext = models.TextField()
    admintext = models.TextField()
    chatdatetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.usertext + "&" + self.admintext