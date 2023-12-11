# chat/tests/test_views.py
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from chat.entity.models import ChatRoom, GroupMessage
from chat.controller.serializers import GroupMessageSerializer
from django.conf import settings

User = get_user_model()

class ListMessagesViewTest(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(email='testuser@gmail.com', password='testpassword@1223')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.chat_room = ChatRoom.objects.create(name='Test Room')
        self.message1 = GroupMessage.objects.create(sender=self.user, chat_room=self.chat_room, content='Message 1')
        self.message2 = GroupMessage.objects.create(sender=self.user, chat_room=self.chat_room, content='Message 2')

        
        self.URL = reverse('list-messages', kwargs={'chat_room_id': self.chat_room.id})

    def test_list_messages(self):
        
        response = self.client.get(self.URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the serializer data matches the expected data
        serializer = GroupMessageSerializer([self.message1, self.message2], many=True)
        self.assertEqual(response.data['results'], serializer.data)

    def test_list_messages_pagination(self):
        # Create additional messages to test pagination
        for i in range(103):
            GroupMessage.objects.create(sender=self.user, chat_room=self.chat_room, content=f'Message {i + 3}')

        
        response = self.client.get(self.URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if pagination is present
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)

        page_size = settings.REST_FRAMEWORK['PAGE_SIZE']

        # Check if the number of results matches the expected number of messages per page
        self.assertEqual(len(response.data['results']), page_size)
