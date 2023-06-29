from pyglet.canvas import Display
#
display = Display(x_screen=1)

from psychopy_pixx.calibration.trackpixx import show_eyepos


if __name__ == "__main__":
    from psychopy.visual import Window
    from pypixxlib.tracker import TRACKPixx3
    window = Window(
        screen=1,
        fullscr=True,
    )
    tracker = TRACKPixx3()
    show_eyepos(window, tracker)
