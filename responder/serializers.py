from rest_framework import serializers, fields
from django.utils import timezone
from datetime import datetime
from .models import TgMessages
from django.conf import settings
from rest_framework.settings import api_settings


class MsgSendSerializer(serializers.ModelSerializer):

    class Meta:
        model = TgMessages
        fields = [
            'msgtext',
            ]

