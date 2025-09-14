import platform
import os
from logging import getLogger
from src.interfaces.interface import Interface
from src.interfaces.st7789_interface import ST7789Interface
from src.interfaces.pygame_interface import PygameInterface

logger = getLogger(__name__)


class InterfaceFactory:
    WIDTH = 240
    HEIGHT = 240
    ROTATION = 90
    PORT = 0
    CS = 1
    DC = 9
    BACKLIGHT_PORT = 13
    SPI_SPEED_HZ = 80_000_000
    WINDOW_TITLE = "Nightscout Display"

    @classmethod
    def create_interface(cls) -> Interface:
        if InterfaceFactory._is_raspberry_pi() and ST7789Interface.is_available():
            try:
                return ST7789Interface(
                    width=cls.WIDTH,
                    height=cls.HEIGHT,
                    rotation=cls.ROTATION,
                    port=cls.PORT,
                    cs=cls.CS,
                    dc=cls.DC,
                    backlight=cls.BACKLIGHT_PORT,
                    spi_speed_hz=cls.SPI_SPEED_HZ,
                )
            except Exception as e:
                logger.debug(f"Failed to initialize ST7789 display: {e}")
                logger.debug("Falling back to Pygame display...")

        # Fall back to Pygame for development
        if PygameInterface.is_available():
            return PygameInterface(
                width=cls.WIDTH,
                height=cls.HEIGHT,
                window_title=cls.WINDOW_TITLE,
            )

        # If nothing works, raise an error
        raise RuntimeError(
            "No suitable display backend available. "
            "Please install either 'st7789' (for Raspberry Pi) or 'pygame' (for development)."
        )

    @staticmethod
    def _is_raspberry_pi() -> bool:
        try:
            if os.path.exists("/proc/device-tree/model"):
                with open("/proc/device-tree/model", "r") as f:
                    model = f.read().lower()
                    return "raspberry pi" in model

            if os.path.exists("/proc/cpuinfo"):
                with open("/proc/cpuinfo", "r") as f:
                    cpuinfo = f.read().lower()
                    return "raspberry pi" in cpuinfo or "bcm" in cpuinfo

        except Exception:
            pass

        machine = platform.machine().lower()
        return machine.startswith("arm") or machine.startswith("aarch")

    @staticmethod
    def get_available_backends() -> dict[str, bool]:
        return {
            "st7789": ST7789Interface.is_available(),
            "pygame": PygameInterface.is_available(),
        }
