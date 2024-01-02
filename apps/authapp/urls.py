# authentication/urls.py
from django.urls import path, include
from . import views as _views 
from oauth2_provider.views import TokenView, RevokeTokenView, IntrospectTokenView

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', _views.RegistrationView.as_view(), name='register'),
    path('users/', _views.UserListView.as_view(), name='user-list'),
    path('my-profile/', _views.ProfileView.as_view(), name='my-profile'),
    path('protected/', _views.ProtectedResourceView.as_view(), name='protected'),

    path('access-token/', _views.GetAccessTokenView.as_view(), name='access-token'),  # gettoken
    path('revoke-token/', RevokeTokenView.as_view(), name='revoke-token'),  # revoketoken
    path('refresh-token/', IntrospectTokenView.as_view(), name='refresh-token'),  # refreshtoken

    # xml-http login
    path('sign-up', _views.RegisterView.as_view(), name='signup'),
    path('login', _views.LoginView.as_view(), name='login'),
    path('logout', _views.logout_view, name='logout'),
    # path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]