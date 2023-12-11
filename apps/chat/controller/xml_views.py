
from chat.entity.models import ChatRoom
from django.views.generic import DetailView, ListView, UpdateView

from chat.service.mixins.chat_view_mixins import GroupMemberRequiredMixin

class InRoomView(GroupMemberRequiredMixin, DetailView):
    template_name = 'chat/chatroom.html'
    model = ChatRoom
    context_object_name = 'chat_room'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['room_name'] = self.object.name
        context['room_messages'] = self.object.group_messages.all()[:100]
        return context
    

class HomeView(ListView):
    model = ChatRoom
    template_name = 'chat/index.html'
    context_object_name = 'chat_rooms'

