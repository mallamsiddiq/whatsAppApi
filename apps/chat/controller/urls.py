# urls.py
from django.urls import path
from django.views.generic import TemplateView

from . import api_views
from . import xml_views

urlpatterns = [
    path('api/chatrooms/', api_views.ChatRoomListCreateView.as_view(), name='chatroom-list-create'),
    path('api/chatrooms/<int:pk>/', api_views.ChatRoomDetailView.as_view(), name='chatroom-detail'),
    path('api/chatrooms/<int:pk>/leave/', api_views.LeaveChatRoomView.as_view(), name='leave-chatroom'),
    path('api/chatrooms/<int:pk>/enter/', api_views.EnterChatRoomView.as_view(), name='enter-chatroom'),
    path('api/chatrooms/<int:chat_room_id>/messages/', api_views.ListMessagesView.as_view(), name='list-messages'),

    # xml http routing
    path('home', xml_views.HomeView.as_view(), name='home'),
    path('chatroom/<int:pk>/', xml_views.InRoomView.as_view(), name='chat-room-inside'),
]
