"""
WSGI config for example_channels project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import channels.asgi

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example_channels.settings")

application = get_wsgi_application()
channel_layer = channels.asgi.get_channel_layer()
