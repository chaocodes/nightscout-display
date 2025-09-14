from src.interfaces.interface import Interface
from src.interfaces.errors import InterfaceClosedError
from src.interfaces.events import InterfaceEvents
from PIL import Image

try:
    import pygame
    import numpy as np

    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False


class PygameInterface(Interface):
    CLOCK_TICK = 60

    def __init__(
        self,
        width: int,
        height: int,
        window_title: str,
    ):
        if not PYGAME_AVAILABLE:
            raise ImportError(
                "pygame library not available. Install with: pip install pygame"
            )

        super().__init__(width, height)

        self.window_width = width
        self.window_height = height

        pygame.init()
        pygame.display.set_caption(window_title)

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.clock = pygame.time.Clock()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise InterfaceClosedError("Pygame window closed")
            elif event.type == pygame.KEYDOWN:
                self._handle_key_press(event.key)

    def _handle_key_press(self, key: int) -> None:
        if key == pygame.K_1:
            self._trigger_event(InterfaceEvents.TOGGLE_MUTE)
        elif key == pygame.K_2:
            self._trigger_event(InterfaceEvents.ACKNOWLEDGE_ALARM)
        elif key == pygame.K_3:
            self._trigger_event(InterfaceEvents.INCREASE_BRIGHTNESS)
        elif key == pygame.K_4:
            self._trigger_event(InterfaceEvents.DECREASE_BRIGHTNESS)

    def update(self, image: Image.Image) -> None:
        self._handle_events()
        img_array = np.array(image)
        surface = pygame.surfarray.make_surface(img_array.swapaxes(0, 1))
        self.screen.blit(surface, (0, 0))
        pygame.display.flip()
        self.clock.tick(self.CLOCK_TICK)

    def cleanup(self) -> None:
        pygame.quit()

    @staticmethod
    def is_available() -> bool:
        return PYGAME_AVAILABLE
