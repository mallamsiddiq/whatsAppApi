from django.contrib.auth import get_user_model
from django.test import TestCase
from chat.entity.models import ChatRoom, GroupMessage, GroupMembership
from chat.controller.serializers import ChatRoomDetailSerializer, GroupMessageSerializer

User = get_user_model()

class ChatRoomDetailSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@gmail.com', password='testpassword@1223')
        self.chat_room = ChatRoom.objects.create(name='Test Room', max_members=2)
        GroupMembership.objects.create(member = self.user, room = self.chat_room)
        self.messages = [
            GroupMessage.objects.create(sender=self.user, chat_room=self.chat_room, content=f'Message {i}')
            for i in range(40)
        ]

    def test_chat_room_detail_serializer(self):
        # Use the serializer to serialize the chat room instance
        serialized_data = ChatRoomDetailSerializer(instance=self.chat_room).data

        # Check if the 'group_messages' field contains only the latest 30 messages
        self.assertIn('group_messages', serialized_data)
        self.assertEqual(len(serialized_data['group_messages']), 30)

        # Create another serializer for comparison if needed
        expected_serializer = ChatRoomDetailSerializer(instance=self.chat_room)
        expected_data = expected_serializer.data

        # Compare the serialized data with the expected data
        self.assertEqual(serialized_data, expected_data)
