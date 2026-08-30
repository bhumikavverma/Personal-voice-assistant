import datetime
import os
import pyautogui
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER

# Volume control helper functions
def set_volume(action: str) -> str:
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        
        current_scalar = volume.GetMasterVolumeLevelScalar()
        
        if "up" in action or "increase" in action:
            new_scalar = min(1.0, current_scalar + 0.15)
            volume.SetMasterVolumeLevelScalar(new_scalar, None)
            return "Increasing volume"
        elif "down" in action or "decrease" in action:
            new_scalar = max(0.0, current_scalar - 0.15)
            volume.SetMasterVolumeLevelScalar(new_scalar, None)
            return "Decreasing volume"
        elif "mute" in action:
            volume.SetMute(1, None)
            return "Muted the system"
        elif "unmute" in action:
            volume.SetMute(0, None)
            return "Unmuted the system"
    except Exception as e:
        return f"Could not adjust volume: {str(e)}"
    return "Volume command not recognized"

def take_screenshot() -> str:
    try:
        # Desktop par screenshot save karega
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_path = os.path.join(desktop_path, f"AURA_screenshot_{timestamp}.png")
        
        screenshot = pyautogui.screenshot()
        screenshot.save(file_path)
        return "Screenshot taken and saved to your desktop"
    except Exception as e:
        return f"Failed to take screenshot: {str(e)}"

def get_time() -> str:
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    return f"The current time is {current_time}"

def get_date() -> str:
    current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
    return f"Today's date is {current_date}"

def open_application(app_name: str) -> str:
    app_name = app_name.lower()
    if "notepad" in app_name:
        os.system("notepad")
        return "Opening Notepad"
    elif "code" in app_name or "vs code" in app_name:
        os.system("code")
        return "Opening Visual Studio Code"
    else:
        return f"Sorry, I cannot open {app_name}"