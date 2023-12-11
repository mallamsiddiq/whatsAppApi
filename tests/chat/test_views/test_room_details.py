from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from chat.entity.models import ChatRoom, GroupMembership, GroupMessage
from chat.controller.serializers import ChatRoomDetailSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatRoomDetailViewTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(email='testuser@gmail.com', password='testpassword@1223')

        # Set up the API client
        self.client = APIClient()
        
        # Create a chat room
        self.chat_room = ChatRoom.objects.create(name='Room 1')
        self.adminmembership = GroupMembership.objects.create(room=self.chat_room, member=self.user, user_perm = 'admin')

        # Add members to the chat room
        self.member1 = User.objects.create_user(email='member1@gmail.com', password='testpassword@1223')
        member2 = User.objects.create_user(email='member2@gmail.com', password='testpassword@1223')

        GroupMembership.objects.create(room=self.chat_room, member=self.member1)
        GroupMembership.objects.create(room=self.chat_room, member=member2)

        # Add a group message to the chat room
        GroupMessage.objects.create(chat_room=self.chat_room, sender=self.member1, content='Hello, Admin!')
        GroupMessage.objects.create(chat_room=self.chat_room, sender=self.user, content='Hello, members!')

        

    def test_retrieve_chat_room_details(self):
        # Log in the user
        self.client.force_authenticate(user=self.user)

        # Make a GET request to retrieve chat room details
        response = self.client.get(f'/api/chatrooms/{self.chat_room.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate the response data based on the serializer structure
        self.assertEqual(response.data['id'], self.chat_room.id)
        self.assertEqual(response.data['name'], 'Room 1')
        self.assertEqual(response.data['max_members'], self.chat_room.max_members)
        self.assertEqual(response.data['date_created'], self.chat_room.date_created.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
        # Add more assertions based on your serializer and model structure

        # Validate members data
        self.assertEqual(len(response.data['members']), 3)  # Including admin
        # Add more assertions based on your serializer and model structure

        # Validate group messages data
        self.assertEqual(len(response.data['group_messages']), 2)
        # Add more assertions based on your serializer and model structure

    def test_retrieve_chat_room_not_a_member(self):

        self.adminmembership.delete()

        self.client.force_authenticate(user=self.user)

        # Attempt to leave the new chat room without being a member
        response = self.client.get(f'/api/chatrooms/{self.chat_room.id}/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_chat_room_unauth(self):

        # Attempt to leave the new chat room without being a member
        response = self.client.get(f'/api/chatrooms/{self.chat_room.id}/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    
    def test_follwed_messages_count(self):
        
        self.client.force_authenticate(user=self.user)

        self.messages = [
            GroupMessage.objects.create(sender=self.user, chat_room=self.chat_room, content=f'Message {i}')
            for i in range(40)
        ]

        # Attempt to leave the new chat room without being a member
        response = self.client.get(f'/api/chatrooms/{self.chat_room.id}/')


        
        self.assertEqual(len(response.data['group_messages']), 30)

