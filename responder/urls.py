from django.urls import path
from . import views


app_name = 'responder'

urlpatterns = [
    path("", views.index, name="index"),
    path('add_msg_api/', views.add_msg_api, name='add_msg_api'),
    path('get_msg_api/', views.get_msg_api, name='get_msg_api'),
]