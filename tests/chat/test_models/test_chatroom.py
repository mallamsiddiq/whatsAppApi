# chat/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from chat.entity.models import ChatRoom, GroupMembership

User = get_user_model()

class ChatRoomModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email='testuser1@gmail.com', password='testpassword@1223')
        self.user2 = User.objects.create_user(email='testuser2@gmail.com', password='testpassword@1223')
        self.user3 = User.objects.create_user(email='testuser3@gmail.com', password='testpassword@1223')
        self.user4 = User.objects.create_user(email='testuser4@gmail.com', password='testpassword@1223')

        self.chat_room = ChatRoom.objects.create(name='Test Room', max_members=2)
        self.membership1 = GroupMembership.objects.create(member=self.user1, room=self.chat_room)

    def test_is_full(self):
        self.assertFalse(self.chat_room.is_full())

        membership2 = GroupMembership.objects.create(member=self.user2, room=self.chat_room)
        self.assertTrue(self.chat_room.is_full())

    def test_user_in_room(self):
        self.assertTrue(self.chat_room.user_in_room(self.user1.id))

    def test_user_is_valid_in(self):
        valid, reason = self.chat_room.user_is_valid_in(self.user1.id)
        self.assertFalse(valid)
        self.assertEqual(reason, "User is already a member of this chatroom.")

        self.membership1.delete()  # Remove the user from the room
        GroupMembership.objects.create(member=self.user2, room=self.chat_room)
        GroupMembership.objects.create(member=self.user3, room=self.chat_room)
        
        valid, reason = self.chat_room.user_is_valid_in(self.user1.id)
        self.assertFalse(valid)
        self.assertEqual(reason, 'Room is already filled')
