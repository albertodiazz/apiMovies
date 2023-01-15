from django.urls import re_path

from . import consumers

# re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
# re_path("chat/", consumers.ChatConsumer.as_asgi()),
websocket_urlpatterns = [
    re_path("chat/", consumers.ChatConsumer.as_asgi()),
]
