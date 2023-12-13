import json
import pytest
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from django.test import TestCase
from chat.controller.serializers import GroupMessageSerializer
from chat.entity.models import ChatRoom, GroupMessage
from chat.consumers import ChatRoomConsumer
from core.asgi import application as asgi_app

User = get_user_model()


@pytest.mark.asyncio
class ChatRoomConsumerTests(TestCase):

    """def setUp(self):
        self.user = User.objects.create_user(email='test_user@gmail.com', password='test_password1!')
        self.room = ChatRoom.objects.create(name='Test Room')
        self.websocket_path = f'/ws/chat/{self.room.id}/'
        self.application = asgi_app

    async def connect_and_authenticate(self, communicator):
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
        message = await communicator.receive_json_from()
        self.assertEqual(message['type'], 'websocket.accept')
        return communicator

    async def test_connect_and_disconnect(self):
        
        communicator = WebsocketCommunicator(self.application, self.websocket_path)
        # await self.connect_and_authenticate(communicator)
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
        message = await communicator.receive_json_from()
        self.assertEqual(message['type'], 'websocket.accept')
        # return communicator
        await communicator.disconnect()"""

    # async def test_receive_message(self):
    #     communicator = WebsocketCommunicator(self.application, self.websocket_path)
    #     communicator = await self.connect_and_authenticate(communicator)

    #     # Send a message
    #     message_data = {'message': 'Test message'}
    #     await communicator.send_json_to(message_data)

    #     # Receive the message
    #     response_data = await communicator.receive_json_from()
    #     payload = response_data['payload']
    #     self.assertIn('id', payload)  # Check if the message has an 'id' field
    #     self.assertEqual(payload['content'], message_data['message'])

    #     # Disconnect
    #     await communicator.disconnect()

    # async def test_receive_message_with_attachment(self):
    #     communicator = WebsocketCommunicator(self.application, self.websocket_path)
    #     communicator = await self.connect_and_authenticate(communicator)

    #     # Send a message with attachment
    #     attachment_data = {'name': 'test.txt', 'data': 'dGVzdCBtZXNzYWdl'}  # Base64 encoded 'test message'
    #     message_data = {'message': 'Test message with attachment', 'attachment': attachment_data}
    #     await communicator.send_json_to(message_data)

    #     # Receive the message
    #     response_data = await communicator.receive_json_from()
    #     payload = response_data['payload']
    #     self.assertIn('id', payload)
    #     self.assertEqual(payload['content'], message_data['message'])

    #     # Check if the attachment is saved
    #     message_id = payload['id']
    #     saved_message = GroupMessage.objects.get(id=message_id)
    #     self.assertIsNotNone(saved_message.attachment)

    #     # Disconnect
    #     await communicator.disconnect()