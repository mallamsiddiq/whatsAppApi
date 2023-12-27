from chat.entity.models import ChatRoom, DirectMessage
from django.views.generic import DetailView, ListView, TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


from chat.service.mixins.chat_view_mixins import GroupMemberRequiredMixin, LoginRequiredMixin
    
class HomeView(TemplateView):
    model = ChatRoom
    template_name = 'chat/index.html'


class DashboardView(LoginRequiredMixin, DetailView):
    template_name = 'chat/dashboard.html'
    model = User

    def get_object(self, queryset=None):
        # Return the currently logged-in user
        return self.request.user


class MyRoomsView(LoginRequiredMixin, ListView):
    model = ChatRoom
    template_name = 'chat/rooms.html'
    context_object_name = 'chat_rooms'

    def get_queryset(self):
        # Assuming get_direct_contacts is a method in your User model
        return self.request.user.my_groups.all()

class MyContactsView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'chat/contacts.html'
    context_object_name = 'contacts'

    def get_queryset(self):
        # Assuming get_direct_contacts is a method in your User model
        return self.request.user.get_direct_contacts


class InRoomView(GroupMemberRequiredMixin, DetailView):
    template_name = 'chat/chatroom.html'
    model = ChatRoom
    context_object_name = 'chat_room'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['room_name'] = self.object.slug_name
        context['room_messages'] = self.object.group_messages.all()[:100]
        return context

class DirectMessageView(LoginRequiredMixin, DetailView):
    template_name = 'chat/direct_msg.html'
    model = User
    context_object_name = 'recipient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        direct_messages =  DirectMessage.objects.filter(
            (Q(recipient=self.object) & Q(sender=self.request.user))\
                | (Q(sender=self.object) & Q(recipient=self.request.user))
            ).order_by('timestamp')[:100]
        
        context['direct_messages'] = direct_messages
        self.object.received_direct_messages.filter(sender = self.request.user)[:100]
        
        return context
    

class RoomMeetingView(GroupMemberRequiredMixin, DetailView):
    template_name = 'chat/video_conference.html'
    model = ChatRoom
    context_object_name = 'chat_room'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['room_name'] = self.object.slug_name
        return context
    
class OneOnOneMeetingView(LoginRequiredMixin, DetailView):
    template_name = 'chat/video_conference.html'
    model = User
    context_object_name = 'recipient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_ids = sorted((self.object.slug_name, self.request.user.slug_name))
        
        context['room_name'] = f"meeting__{user_ids[0]}__{user_ids[1]}"
        return context

@login_required
def join_meeting(request):
    if request.method == 'POST':
        roomID = request.POST['roomID']
        return redirect("/meeting?roomID=" + roomID)
    return render(request, 'joinroom.html')