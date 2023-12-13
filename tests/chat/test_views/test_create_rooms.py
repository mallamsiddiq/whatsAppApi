from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

from chat.entity.models import ChatRoom, GroupMembership
from chat.controller.serializers import ChatRoomListSerializer

User = get_user_model()

class ChatRoomListCreateViewTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(email='testuser@gmail.com', password='testpassword@1223')

        # Set up the API client
        self.client = APIClient()

        # Log in the user
        

    def test_create_chat_room_and_membership(self):
        self.client.force_authenticate(user=self.user)
        # Ensure the initial count of chat rooms and memberships
        initial_chat_room_count = ChatRoom.objects.count()
        initial_membership_count = GroupMembership.objects.count()

        # Create a new chat room using the API
        response = self.client.post('/api/chatrooms/', {'name': 'Test Room'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that a new chat room and membership have been created
        self.assertEqual(ChatRoom.objects.count(), initial_chat_room_count + 1)
        self.assertEqual(GroupMembership.objects.count(), initial_membership_count + 1)

        # Check that the chat room has the correct attributes
        chat_room = ChatRoom.objects.latest('id')
        self.assertEqual(chat_room.name, 'Test Room')
        self.assertEqual(chat_room.members.count(), 1)
        self.assertEqual(chat_room.members.first(), self.user)

        # Check that the membership has been created with the correct attributes
        membership = GroupMembership.objects.latest('id')
        self.assertEqual(membership.room, chat_room)
        self.assertEqual(membership.member, self.user)
        self.assertEqual(membership.user_perm, GroupMembership.UserPermChoice.ADMIN)

    def test_create_chat_room_unauthenticated(self):

        # Attempt to create a new chat room without authentication
        response = self.client.post('/api/chatrooms/', {'name': 'Test Room'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Ensure that no new chat room or membership has been created
        self.assertEqual(ChatRoom.objects.count(), 0)
        self.assertEqual(GroupMembership.objects.count(), 0)


    def test_list_chat_rooms(self):
        
        self.client.force_authenticate(user=self.user)
        # Create some chat rooms and add the user as a member
        chat_room_1 = ChatRoom.objects.create(name='Room 1',)
        GroupMembership.objects.create(room=chat_room_1, member=self.user)

        chat_room_2 = ChatRoom.objects.create(name='Room 2',)
        GroupMembership.objects.create(room=chat_room_2, member=self.user)

        ChatRoom.objects.create(name='Room 3',)

        # Make a GET request to list chat rooms
        response = self.client.get('/api/chatrooms/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(ChatRoom.objects.count(), 3)


        # Validate that the listed chat rooms are the ones the user is a member of
            
        self.assertEqual(response.data['results'][0]['id'], chat_room_1.id)
        self.assertEqual(response.data['results'][1]['id'], chat_room_2.id)
