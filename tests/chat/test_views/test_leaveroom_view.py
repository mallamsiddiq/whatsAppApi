from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from chat.entity.models import ChatRoom, GroupMembership
from django.contrib.auth import get_user_model

User = get_user_model()

class LeaveChatRoomViewTest(TestCase):
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

    def test_leave_chat_room(self):
        # Make a PATCH request to leave the chat room
        response = self.client.patch(f'/api/chatrooms/{self.chat_room.id}/leave/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.chat_room.members.filter(id=self.user.id).exists())
        self.assertFalse(GroupMembership.objects.filter(room=self.chat_room, member=self.user).exists())

    def test_leave_chat_room_unauthenticated(self):
        # Log out the user to simulate an unauthenticated request
        self.client.force_authenticate(user=None)

        # Attempt to leave the chat room without authentication
        response = self.client.patch(f'/api/chatrooms/{self.chat_room.id}/leave/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_leave_chat_room_not_a_member(self):
        # Create a new chat room without adding the user as a member
        other_chat_room = ChatRoom.objects.create(name='Room 2')

        # Attempt to leave the new chat room without being a member
        response = self.client.patch(f'/api/chatrooms/{other_chat_room.id}/leave/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertTrue(self.chat_room.members.filter(id=self.user.id).exists())