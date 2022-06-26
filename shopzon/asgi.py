"""
ASGI config for shopzon project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
import utils.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopzon.settings')

# application = get_asgi_application()

application = ProtocolTypeRouter({
  'http' : get_asgi_application(),
  'websocket': URLRouter( 
    utils.routing.websocket_urlpatterns
  ),
})
