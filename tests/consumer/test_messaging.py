from django.test import TestCase
from channels.testing import WebsocketCommunicator
from chat.consumers import ChatRoomConsumer

# chat/tests/test_consumers.py
import json
import base64
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from channels.layers import get_channel_layer
from chat.entity.models import ChatRoom, GroupMessage
from chat.consumers import ChatRoomConsumer


    

User = get_user_model()

async def connect_user_and_room(communicator, user, room_id):
    channel_layer = get_channel_layer()
    room_group_name = f"chat_{room_id}"

    # Join room group
    await channel_layer.group_add(
        room_group_name, communicator.channel_name
    )

    # Connect to the WebSocket
    connected, _ = await communicator.connect()
    assert connected

    # Authenticate the user
    await communicator.send_json_to({
        "type": "authenticate",
        "user": str(user.id),
        "room_id": room_id,
    })

    response = await communicator.receive_json_from()

    assert response["type"] == "authenticated"
    return communicator

async def disconnect_user_and_room(communicator, room_id):
    channel_layer = get_channel_layer()
    room_group_name = f"chat_{room_id}"

    # Disconnect from the WebSocket
    await communicator.disconnect()

    # Leave room group
    await channel_layer.group_discard(
        room_group_name, communicator.channel_name
    )

async def send_message(communicator, message, attachment=None):
    await communicator.send_json_to({
        "type": "chat.message",
        "message": message,
        "attachment": attachment,
    })

async def receive_message(communicator):
    response = await communicator.receive_json_from()
    assert response["type"] == "chat_message"
    return response["payload"]



class TestWebSockets(TestCase):

    async def test_chat_room_consumer():
        user = User.objects.create_user(username="testuser", password="testpassword")
        room = ChatRoom.objects.create(name="Test Room", max_members=10)

        communicator = WebsocketCommunicator(ChatRoomConsumer.as_asgi())
        
        # Connect user to the room
        await connect_user_and_room(communicator, user, room.id)

        # Test sending and receiving a text message
        message_content = "Hello, World!"
        await send_message(communicator, message_content)
        received_message = await receive_message(communicator)
        assert received_message["sender"]["id"] == str(user.id)
        assert received_message["content"] == message_content

        # Test sending and receiving a message with attachment
        image_data = base64.b64encode(b"fake_image_data").decode("utf-8")
        await send_message(communicator, "Image Attachment", attachment=image_data)
        received_message_with_attachment = await receive_message(communicator)
        assert received_message_with_attachment["sender"]["id"] == str(user.id)
        assert received_message_with_attachment["content"] == "Image Attachment"
        assert "attachment" in received_message_with_attachment

        # Disconnect the user from the room
        await disconnect_user_and_room(communicator, room.id)

        # Connect a user to the room and send a message
        user2 = User.objects.create_user(username="testuser2", password="testpassword")
        await connect_user_and_room(communicator, user2, room.id)
        await send_message(communicator, "Hello from User2")

        # Receive the message as the first user
        received_message_user2 = await receive_message(communicator)
        assert received_message_user2["sender"]["id"] == str(user2.id)
        assert received_message_user2["content"] == "Hello from User2"

        # Disconnect the second user from the room
        await disconnect_user_and_room(communicator, room.id)
