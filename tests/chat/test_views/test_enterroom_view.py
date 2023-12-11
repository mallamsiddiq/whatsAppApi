from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from chat.entity.models import ChatRoom, GroupMembership
from django.contrib.auth import get_user_model

User = get_user_model()

class EnterChatRoomViewTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(email='testuser@gmail.com', password='testpassword@1223')
        # Create a chat room and add the user as a member
        self.chat_room = ChatRoom.objects.create(name='Room 1')
        self.membership = GroupMembership.objects.create(room=self.chat_room, member=self.user)

        # Set up the API client
        self.client = APIClient()

        # Log in the user
        self.client.force_authenticate(user=self.user)

    def test_enter_chat_room(self):
        # Create a new chat room
        new_chat_room = ChatRoom.objects.create(name='Room 2')

        # Make a PATCH request to enter the new chat room
        response = self.client.patch(f'/api/chatrooms/{self.chat_room.id}/enter/')
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(new_chat_room.members.filter(id=self.user.id).exists())
        self.assertTrue(GroupMembership.objects.filter(room=new_chat_room, member=self.user).exists())


    def test_enter_chat_room_already_a_member(self):
        # Attempt to enter the chat room where the user is already a member
        response = self.client.patch(f'/api/chatrooms/{self.chat_room.id}/enter/')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'User is already a member of this chatroom.')
        self.assertTrue(self.chat_room.members.filter(id=self.user.id).exists())
        self.assertTrue(GroupMembership.objects.filter(room=self.chat_room, member=self.user).exists())


    def test_enter_chat_room_full(self):
        # Set the max_members count to 1 for the chat room
        self.chat_room.max_members = 1
        self.chat_room.save()

        # Create a new user for testing
        other_user = User.objects.create_user(email='otheruser@gmail.com', password='testpassword@1223')
        # Log in the new user
        self.client.force_authenticate(user=other_user)

        # Attempt to enter the full chat room
        response = self.client.patch(f'/api/chatrooms/{self.chat_room.id}/enter/')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Room is already filled')
        self.assertFalse(self.chat_room.members.filter(id=other_user.id).exists())
        self.assertFalse(GroupMembership.objects.filter(room=self.chat_room, member=other_user).exists())
