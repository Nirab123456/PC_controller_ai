import time
from pynput import keyboard, mouse


class UserInputChecker:
    """Class to check for user input."""
    def __init__(self):
        """Initialize the class."""
        self.keyboard_listener = None
        self.mouse_listener = None
        self.user_input_detected = False

    def start(self):
        """Start the listeners."""
        self.keyboard_listener = keyboard.Listener(on_press=self.on_keyboard_press)
        self.mouse_listener = mouse.Listener(on_move=self.on_mouse_move,
                                             on_click=self.on_mouse_click)
        self.keyboard_listener.start()
        self.mouse_listener.start()

    def stop(self):
        """Stop the listeners."""
        if self.keyboard_listener is not None:
            self.keyboard_listener.stop()
        if self.mouse_listener is not None:
            self.mouse_listener.stop()

    def on_keyboard_press(self, key):
        """Check for keyboard input."""
        self.user_input_detected = True
        self.stop()
        return False

    def on_mouse_move(self, x, y):
        """Check for mouse movement."""
        self.user_input_detected = True
        self.stop()
        return False

    def on_mouse_click(self, x, y, button, pressed):
        """Check for mouse clicks."""
        if pressed:
            self.user_input_detected = True
            self.stop()
            return False
        return True

    def check_input(self):
        """Check for user input."""
        self.user_input_detected = False
        self.start()
        start_time = time.time()
        while not self.user_input_detected and (time.time() - start_time) < 30:
            time.sleep(1)
        self.stop()
        return self.user_input_detected
















# from pynput import keyboard, mouse
# import subprocess
# import time

# class UserInputChecker:
#     def __init__(self):
#         self.keyboard_listener = None
#         self.mouse_listener = None
#         self.user_input_detected = False

#     def start(self):
#         self.keyboard_listener = keyboard.Listener(on_press=self.on_keyboard_press)
#         self.mouse_listener = mouse.Listener(on_move=self.on_mouse_move,
#                                              on_click=self.on_mouse_click)
#         self.keyboard_listener.start()
#         self.mouse_listener.start()

#     def stop(self):
#         if self.keyboard_listener is not None:
#             self.keyboard_listener.stop()
#         if self.mouse_listener is not None:
#             self.mouse_listener.stop()

#     def on_keyboard_press(self, key):
#         self.user_input_detected = True
#         self.stop()
#         return False

#     def on_mouse_move(self, x, y):
#         self.user_input_detected = True
#         self.stop()
#         return False

#     def on_mouse_click(self, x, y, button, pressed):
#         if pressed:
#             self.user_input_detected = True
#             self.stop()
#             return False
#         return True

#     def check_input(self):
#         self.user_input_detected = False
#         self.start()
#         while True:
#             script_path = 'program_exe.py'
#             subprocess.run(['python', script_path])
#             if self.user_input_detected:
#                 break
#         self.stop()
