from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from oauth2_provider.models import AccessToken
from channels.auth import AuthMiddlewareStack

@database_sync_to_async
def get_user(token_key):
    access_token = AccessToken.objects.filter(token=token_key).first()

    if access_token and access_token.user:
        return access_token.user

    return AnonymousUser()

class TokenAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        query_string = scope["query_string"]
        query_params = query_string.decode()
        query_dict = parse_qs(query_params)
        token = query_dict.get("token")
        if token and token[0]:
            token = token[0]
            user = await get_user(token)
            scope["user"] = user
        
        return await self.app(scope, receive, send)

TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))