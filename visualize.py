import os
import threading
import time


class RenderScreen(threading.Thread):
    def __init__(self, func):
        threading.Thread.__init__(self)
        self.running = True
        self.func = func

    def run(self):
        while self.running:
            # Do your rendering here
            refresh()
            self.func()
            # time.sleep(0.2)

    def stop(self):
        self.running = False

    def switch_func(self, func):
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
    """ Used to print the waiting screen."""
    print("Loading...")
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
