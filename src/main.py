import httpx
import logging

from src.clients.nightscout import NightscoutClient
from src.interfaces.factory import InterfaceFactory
from src.app.view import AppView
from src.app.state import AppState
from src.app.controller import AppController

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    http_client = httpx.Client()
    nightscout_client = NightscoutClient(http_client)

    interface = InterfaceFactory.create_interface()
    logger.info(f"Using interface: {type(interface).__name__}")
    logger.info(f"Available interfaces: {InterfaceFactory.get_available_backends()}")

    state = AppState()
    view = AppView(interface.width, interface.height, state)
    controller = AppController(view, state, interface, nightscout_client)

    controller.start()
