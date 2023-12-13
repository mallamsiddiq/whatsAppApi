# server/trips/tests/test_websocket.py

import pytest
from channels.testing import WebsocketCommunicator

from core.asgi import application

TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

@pytest.mark.asyncio
class TestWebSocket:
    async def test_can_connect_to_server(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/ws/chat/1/'
        )
        connected,  subprotocol= await communicator.connect()
        print(subprotocol)
        assert connected is True
        await communicator.disconnect()