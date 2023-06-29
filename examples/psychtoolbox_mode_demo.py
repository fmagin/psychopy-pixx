# This is the magic invocation that creates a pyglet display on the second x_screen
# It will be implicitly cached by pyglet, so subsequent calls to `pyglet.canvas.get_display()`
# will return this Display with the correct x_screen, and not create a new one (which would be on the wrong screen)
# This MUST happen before psychopy is imported, otherwise psychopy will call get_display during import
# and assign the resulting wrong display to internal variables
from pyglet.canvas import Display
display = Display(x_screen=1)


from psychopy import event
from psychopy.visual import Window, Circle

if __name__ == "__main__":
    window = Window(
        # There are two options here, with tradeoffs:
        # fullscr=True, will capture the inputs and make it impossible to focus another window
        # if your script doesn't terminate at some point, you will have to kill it from another terminal
        # the only way to access another terminal is to switch the TTY with Ctrl+Alt+F1, login,
        # and kill the process:
        # For that run `pgrep -fa python3` to find the process id,
        # and then `kill <pid>` where <pid> is the process id shown at the start of each result line of pgrep

        # fullscr=False, will not lock you into the window, but you will have to specify the size of the window manually
        # the psychopy script will be able to read the inputs until you focus another window,
        # but I have not found a way to move the focus _back_ to the psychopy window after
        # so it will be impossible to send keypresses to it after loosing focus
        fullscr=False,
        size=(1920, 1080),
    )

    p = Circle(window, pos=(0, 0), radius=20, units='pix')
    p.draw()
    window.flip()
    event.waitKeys()
