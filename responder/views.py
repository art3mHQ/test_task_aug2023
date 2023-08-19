from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, FileUploadParser, MultiPartParser, FormParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import MsgSendSerializer
from django.contrib import messages

from .models import ChatIdList, TgMessages

import requests
import telebot

bot = telebot.TeleBot('6473686856:AAH12owHqO4fkeoa6pB_s3KDQcay4qeY3GA')

def index(request):
    return HttpResponse("Hello, world. You're at the index.")

@api_view(['POST'])
def add_msg_api(request):
    serializer = MsgSendSerializer(data=request.data)
    try:
        chat_id_obj = ChatIdList.objects.get(user=request.user)
    except ChatIdList.DoesNotExist:
        chat_id_obj = None

    # print(chat_id_value)
    if serializer.is_valid() and chat_id_obj:
        chat_id_value = chat_id_obj.chat_id
        # cos you need generate chat_id AFTER generating token lets take msg_aka_token from db and generate token
        if chat_id_value == 0:

            msg_aka_token = chat_id_obj.first_msg_token
            r = requests.get(url = 'https://api.telegram.org/bot6473686856:AAH12owHqO4fkeoa6pB_s3KDQcay4qeY3GA/getUpdates')
            data = r.json()

            # Iterate through each result in the 'result' list
            for result in data["result"]:
                # Check if the 'text' property in the message dictionary is "fff"
                if result["message"]["text"] == msg_aka_token:
                    chat_id_value = result["message"]["chat"]["id"]
                    print("Chat ID:", chat_id_value)
                    break  # Exit loop after finding the first match

        # send msg to users chat
        msg = f"{request.user.name}, я получил от тебя сообщение: \n{serializer.validated_data.get('msgtext')}"
        bot.send_message(chat_id_value, msg)
        # save to db
        newmsg = serializer.save(user=request.user)

        messages.success(request, 'Msg saved (and kinda sent) successful')
        return JsonResponse(newmsg.id, status=201, safe=False)
    
    elif serializer.is_valid():
        msg_aka_token = serializer.validated_data.get("msgtext")

        # lets save first msg aka token to db
        c = ChatIdList(user=request.user, chat_id=0, first_msg_token=msg_aka_token) 
        c.save()

        messages.success(request, 'TOKEN creation successful')
        return JsonResponse(serializer.data, status=201, safe=False)
    return JsonResponse(serializer.errors, status=400)

@api_view(['GET'])
def get_msg_api(request):
    if request.user.is_authenticated:
        allmessages = TgMessages.objects.filter(user=request.user).values("created","msgtext")
        data = list(allmessages)
        data.reverse()
        print('hi there')
        print(data)
        return JsonResponse(data, status=200, safe=False)
    return JsonResponse(serializer.errors, status=400)







