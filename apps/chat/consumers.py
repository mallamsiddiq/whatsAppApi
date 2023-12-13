import base64
import json
import secrets
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from chat.entity.models import GroupMessage, ChatRoom
from chat.controller.serializers import GroupMessageSerializer

from django.shortcuts import get_object_or_404



class IsUserAndInRoom:
    def check_auth(self):
        # authentication logic here
        print("Authenticating")
        if not self.user.is_authenticated or not self.chat_room.user_in_room(self.user.id):
            self.close()  # Disconnect the WebSocket if not authenticated
            return
        
        print("Access Granted")

class ChatRoomConsumer(IsUserAndInRoom, WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.room_id = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_id}"
        self.chat_room = get_object_or_404(ChatRoom, id=int(self.room_id))

        self.check_auth()

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        # parse the json data into dictionary object
        text_data_json = json.loads(text_data)

        payload = self.handle_message(text_data_json)

        text_data_json['payload'] = payload

        # Send message to room group
        chat_type = {"type": "chat_message"}
        return_dict = {**chat_type, **text_data_json}
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            return_dict,
        )

    def handle_message(self, data):
        message, attachment = data.get("message", ''), data.get("attachment")

        if message or attachment:
            # Save the message to the database
            _message = GroupMessage.objects.create(
                sender=self.user,
                content=message,
                chat_room=self.chat_room,
            )

            # Handle file attachment, if any
            if attachment:
                file_data = base64.b64decode(attachment['data'])
                file_name = f"{secrets.token_urlsafe(10)}_{attachment['name']}"
                file_path = default_storage.save(file_name, ContentFile(file_data))
                _message.attachment.name = file_path
                _message.save()

            # Serialize and return the message data
            serializer = GroupMessageSerializer(instance=_message)
            return serializer.data

        return {"error": "empty"}




    # Receive message from room group
    def chat_message(self, event):
        text_data_json = event.copy()
        text_data_json.pop("type")

        self.send(
            text_data=json.dumps(
                event['payload']
            )
        )