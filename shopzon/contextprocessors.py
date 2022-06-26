import time
from random import choice
from store.models import Product
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()

# def notification(request):
#   while(True):
#     product = choice(Product.objects.all())
#     # product = {'product': product}
#     async_to_sync(channel_layer.group_send)(
#       'notification_group',
#       {
#         'type':'send_notification',
#         'product':product,
#       }
#     )
#     return product



def notification(request):
    product = choice(Product.objects.all())
    product = dict({'product':product})
    print(product)
    return product