from pynput import keyboard
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

def toggle_mic():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    
    current_state = volume.GetMute()
    if current_state == 0:
        volume.SetMute(1, None)
        print("Микрофон отключен")
    else:
        volume.SetMute(0, None)
        print("Микрофон включен")

def on_press(key):
    if isinstance(key, keyboard.KeyCode) and key.char == 'a':
        if current_keys == {keyboard.Key.shift, keyboard.Key.cmd}:
            toggle_mic()

def on_release(key):
    try:
        current_keys.remove(key)
    except KeyError:
        pass

def on_press_handler(key):
    current_keys.add(key)
    on_press(key)

current_keys = set()

with keyboard.Listener(on_press=on_press_handler, on_release=on_release) as listener:
    listener.join()