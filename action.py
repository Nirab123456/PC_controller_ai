import psutil
import ctypes
import ctypes
import sys
import os
import ctypes




class Process_task():
    def __init__(self):
        """initate the class class contains (set_brightness, is_admin, hibernate, sleep,close_task,turn_off_screen)"""

        self.process_name= None
        
        pass
    def set_brightness(self,value):
        """set the brightness of the screen"""
        # Define the required constants and structures
        user32 = ctypes.windll.user32
        adj_brightness = value * 65535 // 100  # Convert percentage to brightness value (0-65535)

        # Set the brightness
        user32.SetMonitorBrightness(user32.GetDC(0), adj_brightness)

    def is_admin(self):
        """check if the user is admin or not"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    def hibernate(self):
        """hibernate the pc"""
        try:
            if self.is_admin():
                ctypes.windll.powrprof.SetSuspendState(0, 1, 0)
            else:
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        except Exception as e:
            print(str(e))
            os.system("shutdown /h")

    def sleep(self):
        """sleep the pc"""
        try:
            if self.is_admin():
                ctypes.windll.powrprof.SetSuspendState(0, 0, 0)
            else:
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        except Exception as e:
            print(str(e))
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,0,0")


    def close_task(self):
        """close the task"""
        for process in psutil.process_iter(['name']):
            if process.info['name'] == self.process_name:
                process.kill()
                print(f"Closed task: {self.process_name}")


    def turn_off_screen(self):
        """turn off the screen"""
        # Call the SendMessage function to turn off the screen
        ctypes.windll.user32.SendMessageW(65535, 274, 61808, 2)

