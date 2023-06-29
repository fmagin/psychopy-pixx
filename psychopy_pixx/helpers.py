from typing import Tuple

from psychopy.monitors import Monitor
from psychopy.visual import Window


class CoordinateConverter:
    """
    Terminology:
    Monitorspace is the coordinate system of the monitor, with the origin in the top left corner
    x dimension goes to the right, y dimension goes down

    WindowSpace is the coordinate system of the window, with the origin in the top left corner of the window
    x goes right, y goes down

    The Window has its position in Monitorspace (I think?)

    The PsychoPy coordinate space is in the center of the Window
    x goes right, y goes !UP!

    """
    def __init__(self, window: Window):
        self.window = window

    def pixels_topleft_to_center(self, x: float, y: float) -> Tuple[float, float]:
        # The window pos can be a tuple or a numpy array

        assert (self.window.pos[0], self.window.pos[1]) == (0, 0), f"{self.window.pos}"
        width, height = self.window.size
        return x - width / 2, - (height / 2 + y)





