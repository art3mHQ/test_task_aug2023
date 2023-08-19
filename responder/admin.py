from django.contrib import admin

from .models import TgMessages, ChatIdList

admin.site.register(TgMessages)
admin.site.register(ChatIdList)
