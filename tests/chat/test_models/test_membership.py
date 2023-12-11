# chat/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from chat.entity.models import ChatRoom, GroupMembership
from django.core.exceptions import ValidationError

User = get_user_model()

class GroupMembershipModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@gmail.com', password='testpassword@1223')
        self.user2 = User.objects.create_user(email='testuser2@gmail.com', password='testpassword@1223')
        self.chat_room = ChatRoom.objects.create(name='Test Room', max_members=2)

    def test_save(self):
        GroupMembership.objects.create(
            member=self.user,
            room=self.chat_room
        )
        self.assertEqual(GroupMembership.objects.count(), 1)

        with self.assertRaises(ValidationError) as context:
            GroupMembership.objects.create(
                user_perm=GroupMembership.UserPermChoice.REGULAR,
                member=self.user,
                room=self.chat_room
            )

        self.assertIn(f"User is already a member of this chatroom.", str(context.exception))
        self.assertEqual(GroupMembership.objects.count(), 1)  # Ensure the second membership wasn't created

        GroupMembership.objects.create(
            member=self.user2,
            room=self.chat_room
        )

        self.assertEqual(GroupMembership.objects.count(), 2)


        with self.assertRaises(ValidationError) as context:
            GroupMembership.objects.create(
                user_perm=GroupMembership.UserPermChoice.REGULAR,
                member=self.user,
                room=self.chat_room
            )

        self.assertIn(f"Room is already filled", str(context.exception))
        self.assertEqual(GroupMembership.objects.count(), 2)  # Ensure the second membership wasn't created
