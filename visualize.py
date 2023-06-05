import os
import threading
import time


class RenderScreen(threading.Thread):
    def __init__(self, func):
        threading.Thread.__init__(self)
        self.running = True
        self.func = func

    def run(self):
        """
        Override the run() function of threading.Thread class.
        All the rendering should be written here.
        """
        while self.running:
            # Do your rendering here
            refresh()
            self.func()

    def stop(self):
        """
        Stop the rendering.
        """
        self.running = False

    def switch_func(self, func):
        """
        Switch the function to be rendered.
        """
        self.func = func


def refresh():
    """A function to clear the screen by using the os.system() function.
    :return: None
    """

    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner():
    """ Used to print the banner."""

    print()
    print("--------------------------------------------------------------------------------------------------------")
    print("▄▀▀▀▀▄      ▄▀▀█▄   ▄▀▀▀▀▄   ▄▀▀▄ ▀▀▄      ▄▀▀▄▀▀▀▄  ▄▀▀█▀▄    ▄▀▄▄▄▄   ▄▀▀▄ █  ▄▀▀█▄▄▄▄  ▄▀▀▄▀▀▀▄")
    print("█    █      ▐ ▄▀ ▀▄ █     ▄▀ █   ▀▄ ▄▀     █   █   █ █   █  █  █ █    ▌ █  █ ▄▀ ▐  ▄▀   ▐ █   █   █")
    print("▐    █        █▄▄▄█ ▐ ▄▄▀▀   ▐     █       ▐  █▀▀▀▀  ▐   █  ▐  ▐ █      ▐  █▀▄    █▄▄▄▄▄  ▐  █▀▀█▀ ")
    print("    █        ▄▀   █   █            █          █          █       █        █   █   █    ▌   ▄▀    █ ")
    print("  ▄▀▄▄▄▄▄▄▀ █   ▄▀     ▀▄▄▄▄▀    ▄▀         ▄▀        ▄▀▀▀▀▀▄   ▄▀▄▄▄▄▀ ▄▀   █   ▄▀▄▄▄▄   █     █ ")
    print("  █         ▐   ▐          ▐     █         █         █       █ █     ▐  █    ▐   █    ▐   ▐     ▐ ")
    print("  ▐                              ▐         ▐         ▐       ▐ ▐        ▐        ▐            ")
    print("--------------------------------------------------------------------------------------------------------")
    print()


def waiting():
    """
    Used to print the waiting screen.
    An animation of a falling object.
    """
    print("Calculating the route, please wait patiently...")
    frames = ["""
    -----
    |   |
    | * |
    |   |
    -----
    """, """
    -----
    | * |
    |   |
    |   |
    -----
    """, """
    -----
    |   |
    |   |
    | * |
    -----
    """, """
    -----
    |   |
    |   |
    | * |
    -----
    """]

    for frame in frames:
        print(frame)
        time.sleep(0.2)


def spinner():
    """
    Used to print the waiting screen.
    An animation of a spinner.
    """
    frames = ['|     |', '/     /', '-     -', '\\     \\', '|     |']
    for frame in frames:
        print("Loading the map, please wait patiently..." + frame, end='\r')
        # Print the frame and move the cursor back to the beginning of the line
        time.sleep(0.1)  # Adjust the delay as desired
