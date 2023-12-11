# authapp/views.py
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from . import forms

from .serializers import RegistrationSerializer, UserSerializer, User

class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
        

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class ProtectedResourceView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        return Response({'message': 'Welcome, you re auth !'}, status=status.HTTP_200_OK)
    

from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout

class RegisterView(CreateView):
    form_class = forms.SigupForm
    template_name = 'authapp/signup.html'
    success_url = reverse_lazy('login')

class LoginView(LoginView):
    template_name = 'authapp/login.html'
    success_url = reverse_lazy('home')

    def get_success_url(self):
        redirect_url = self.request.GET.get('next', self.success_url)
        
        return redirect_url


def logout_view(request):
    logout(request)
    return redirect('login')