import ctypes
from ctypes import wintypes

class JOYINFOEX(ctypes.Structure):
    _fields_ = [(name, wintypes.DWORD) for name in (
        "dwSize", "dwFlags", "dwXpos", "dwYpos", "dwZpos", "dwRpos", "dwUpos", "dwVpos",
        "dwButtons", "dwButtonNumber", "dwPOV", "dwReserved1", "dwReserved2",
    )]

JOY_RETURNALL = 0xFF

# DualSense buttons (in HID order) named like their XInput counterparts, so the same gestures work
BUTTON_ITEMS = [
    (0x0001, "X"),  # Square
    (0x0002, "A"),  # Cross
    (0x0004, "B"),  # Circle
    (0x0008, "Y"),  # Triangle
    (0x0010, "LB"),  # L1
    (0x0020, "RB"),  # R1
    (0x0040, "LT"),  # L2
    (0x0080, "RT"),  # R2
    (0x0100, "Back"),  # Create
    (0x0200, "Start"),  # Options
    (0x0400, "L_Thumb"),  # L3
    (0x0800, "R_Thumb"),  # R3
    (0x1000, "PS"),  # PS button
    (0x2000, "Touchpad"),  # Touchpad click
    (0x4000, "Mute"),  # Mute button
]

# D-Pad is a hat switch reporting an angle in 1/100 degree, diagonals press two directions
POV_ITEMS = {
    0: {"Up"},
    4500: {"Up", "Right"},
    9000: {"Right"},
    13500: {"Down", "Right"},
    18000: {"Down"},
    22500: {"Down", "Left"},
    27000: {"Left"},
    31500: {"Up", "Left"},
}

class Joystick:
    def __init__(self):
        self._winmm = ctypes.windll["winmm"]
        self._info = JOYINFOEX(dwSize=ctypes.sizeof(JOYINFOEX), dwFlags=JOY_RETURNALL)

    def read(self):
        """Return the set of pressed buttons, or None if no gamepad is connected."""
        # get gamepad 0
        if self._winmm.joyGetPosEx(0, ctypes.byref(self._info)):
            return None
        pressed = {name for mask, name in BUTTON_ITEMS if self._info.dwButtons & mask}
        return pressed | POV_ITEMS.get(self._info.dwPOV, set())