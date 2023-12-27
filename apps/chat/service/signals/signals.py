# # signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth import get_user_model
# from chat.entity.models import DirectMessage

# User = get_user_model()

# @receiver(post_save, sender=DirectMessage)
# def create_contact_on_first_message(sender, instance, created, **kwargs):
#     """
#     Signal to create add contact when a user sends or receives their first direct message.
#     """
#     if created:
#         sender = instance.sender
#         recipient = instance.recipient

#         # Check if a contact already exists
#         if not sender.direct_contacts.filter(id=recipient.id).exists():
#             # Create a contact for the sender
#             sender.direct_contacts.add(recipient)

#         if not recipient.direct_contacts.filter(id=sender.id).exists():
#             # Create a contact for the recipient
#             recipient.direct_contacts.add(sender)
