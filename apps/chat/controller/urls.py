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
    path('', xml_views.HomeView.as_view(), name='home'),
    path('dashboard', xml_views.DashboardView.as_view(), name='dashboard'),
    path('my-rooms', xml_views.MyRoomsView.as_view(), name='my-rooms'),
    path('my-contacts', xml_views.MyContactsView.as_view(), name='my-contacts'),
    path('chatroom/<int:pk>/', xml_views.InRoomView.as_view(), name='chat-room-inside'),
    path('direct/<int:pk>/', xml_views.DirectMessageView.as_view(), name='direct-msg-inside'),
    path('chatroom/<int:pk>/meeting/', xml_views.RoomMeetingView.as_view(), name='room-meeting'),
    path('direct/<int:pk>/one-one', xml_views.OneOnOneMeetingView.as_view(), name='one-one-meeting'),
    path('join/', xml_views.join_meeting, name='join_room'),
]