import ctypes
from ctypes import wintypes
from .thumbstick import Thumbstick

class XINPUT_GAMEPAD(ctypes.Structure):
    _fields_ = [
        ("wButtons", wintypes.WORD),
        ("bLeftTrigger", ctypes.c_ubyte),
        ("bRightTrigger", ctypes.c_ubyte),
        ("sThumbLX", ctypes.c_short),
        ("sThumbLY", ctypes.c_short),
        ("sThumbRX", ctypes.c_short),
        ("sThumbRY", ctypes.c_short),
    ]

class XINPUT_STATE(ctypes.Structure):
    _fields_ = [
        ("dwPacketNumber", wintypes.DWORD),
        ("Gamepad", XINPUT_GAMEPAD),
    ]

BUTTON_ITEMS = [
    (0x0001, "Up"),
    (0x0002, "Down"),
    (0x0004, "Left"),
    (0x0008, "Right"),
    (0x0010, "Start"),
    (0x0020, "Back"),
    (0x0040, "L_Thumb"),
    (0x0080, "R_Thumb"),
    (0x0100, "LB"),
    (0x0200, "RB"),
    (0x1000, "A"),
    (0x2000, "B"),
    (0x4000, "X"),
    (0x8000, "Y")
]

THRESHOLD_PRESS = 200
THRESHOLD_RELEASE = 30

class XInput:
    def __init__(self):
        self._xinput = ctypes.windll["xinput1_4"]
        self._state = XINPUT_STATE()
        self._lt = self._rt = False
        self._left = Thumbstick("L_Thumb")
        self._right = Thumbstick("R_Thumb")

    def read(self):
        """Return the set of pressed buttons, or None if no gamepad is connected."""
        # get gamepad 0
        if self._xinput.XInputGetState(0, ctypes.byref(self._state)):
            return None
        gp = self._state.Gamepad
        pressed = {name for mask, name in BUTTON_ITEMS if gp.wButtons & mask}
        pressed |= self._left.read(gp.sThumbLX, gp.sThumbLY) | self._right.read(gp.sThumbRX, gp.sThumbRY)
        # LT/RT act as buttons: pressed above THRESHOLD_PRESS, released below THRESHOLD_RELEASE
        self._lt = gp.bLeftTrigger > THRESHOLD_PRESS or (self._lt and gp.bLeftTrigger >= THRESHOLD_RELEASE)
        self._rt = gp.bRightTrigger > THRESHOLD_PRESS or (self._rt and gp.bRightTrigger >= THRESHOLD_RELEASE)
        if self._lt:
            pressed.add("LT")
        if self._rt:
            pressed.add("RT")
        return pressed