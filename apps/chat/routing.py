from django.urls import re_path
from . import consumers, dm_consumers

websocket_urlpatterns = [
    # re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer),
    
    re_path(r'ws/chat-room/(?P<room_name>\w+)/$', consumers.ChatRoomConsumer.as_asgi(), name='ws-chat'),
    re_path(r'ws/chat-direct/(?P<reciepient_id>\w+)/$', dm_consumers.DmMessagingConsumer.as_asgi(), name='ws-chat'),
]