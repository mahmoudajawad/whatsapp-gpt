"""
WhatsGPT Backend

This module bootstraps a AIOHttp server that serves a webhook to listen to WhatsApp API messages
events
"""

import logging
import os

from aiohttp import web
from dotenv import load_dotenv

from endpoints import root_endpoint_handler, webhook_endpoint_handler

# Backend expects following env variables:
# - PORT: If set it will be converted into `int` type to use as port number. If conversion failed,
#   it will be ignored. If not set or ignored, will default to 8080
load_dotenv()


def serve():
    """
    Serves AIOHttp application with root, webhook endpoints
    """

    logging.basicConfig(level=logging.DEBUG)

    port = 8080

    if port_str := os.getenv("PORT"):
        try:
            port = int(port_str)
        except ValueError:
            logging.warning(
                (
                    "Failed to convert env variable 'PORT' of value '%s' to type 'int'. "
                    "Defaulting to 8080"
                ),
                port_str,
            )

    app = web.Application()
    app.add_routes(
        [
            web.get("/", root_endpoint_handler),
            web.post("/webhook", webhook_endpoint_handler),
        ]
    )
    web.run_app(app, port=port)
