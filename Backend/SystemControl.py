from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc
import pyautogui

# Volume control using pycaw
def set_volume(change_percent):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    # Get current volume level
    current = volume.GetMasterVolumeLevelScalar()
    new_level = min(max(current + (change_percent / 100), 0.0), 1.0)
    volume.SetMasterVolumeLevelScalar(new_level, None)

def mute_mic():
    # Simulate "Mic Mute" hotkey (Windows default: Win + Alt + K on some systems)
    pyautogui.hotkey('fn', 'f4')  # Change to your preferred hotkey if needed

def adjust_brightness(change_percent):
    try:
        current = sbc.get_brightness(display=0)
        new_level = min(max(current[0] + change_percent, 0), 100)
        sbc.set_brightness(new_level)
    except Exception as e:
        print(f"❌ Brightness adjustment failed: {e}")
