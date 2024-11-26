from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from celery import shared_task

@shared_task
def send_websocket_notify(group_name, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "notify",
            "message": message,
        },
    )
