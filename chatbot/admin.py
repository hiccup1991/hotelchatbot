from django.contrib import admin

from .models import CustomUser, Theme, CurrentTheme, Message, Room, ChatBotHistory

admin.site.register(CustomUser)
admin.site.register(Theme)
admin.site.register(CurrentTheme)
admin.site.register(Message)
admin.site.register(Room)
admin.site.register(ChatBotHistory)

