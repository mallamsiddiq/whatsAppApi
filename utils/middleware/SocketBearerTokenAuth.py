from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async

from oauth2_provider.models import AccessToken
from channels.middleware import BaseMiddleware

from channels.auth import AuthMiddlewareStack


@database_sync_to_async
def get_user(token_key):
    try:
        access_token = AccessToken.objects.get(token=token_key)
        print(access_token.user, "starting")
        return access_token.user
    except AccessToken.DoesNotExist:
        print('Invalid Token:', token_key)
        return AnonymousUser()


class TokenAuthMiddleware(BaseMiddleware):

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        headers = scope.get('headers')
        if headers:
            headers = dict(headers)
            if headers.get(b'sec-websocket-protocol') and b'authorization' in headers[b'sec-websocket-protocol']:
                _, token_name, token_key = headers[b'sec-websocket-protocol'].decode().split(',')
                if token_name.strip() in {'Token', 'Bearer'}:
                    scope['user'] = await get_user(token_key.strip())
        
        return await self.inner(scope, receive, send)
    


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))