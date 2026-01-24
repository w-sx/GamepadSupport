import threading
import time
import ctypes
from ctypes import wintypes
import inputCore
import globalPluginHandler
import queueHandler
import addonHandler
from logHandler import log

addonHandler.initTranslation()

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

class GamepadGesture(inputCore.InputGesture):
    shouldPreventSystemIdle = True
    def __init__(self, button_name):
        self.button_name = button_name
        super().__init__()
    def _get_identifiers(self): return [f"gp:{self.button_name.lower()}"]
    @classmethod
    def getDisplayTextForIdentifier(cls,identifier): return _("Gamepad Controller"), identifier.split(':')[1]
    def _get_displayName(self): return _("Gamepad") + f" {self.button_name}"

inputCore.registerGestureSource("gp", GamepadGesture)

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def __init__(self):
        super().__init__()
        self._terminate = False
        self._xinput = None
        self.hasGamepad = False
        try:
            self._xinput = ctypes.windll["xinput1_4"]
        except Exception:
            log.error("XInput DLL not found.")
            return
        self._thread = threading.Thread(target=self._run_poll, name="gamepad_poll")
        self._thread.daemon = True
        self._thread.start()

    def _run_poll(self):
        state = XINPUT_STATE()
        last_buttons = 0
        last_lt_state = last_rt_state = False
        THRESHOLD_PRESS = 200
        THRESHOLD_RELEASE = 30

        while not self._terminate:
            try:
                # get gamepad 0
                res = self._xinput.XInputGetState(0, ctypes.byref(state))
                if res == 0:  # ERROR_SUCCESS
                    if not self.hasGamepad:
                        self.hasGamepad = True
                        log.info("Gamepad connected")
                    gp = state.Gamepad
                    # 1. Button
                    curr = gp.wButtons
                    if curr != last_buttons:
                        pressed = (curr ^ last_buttons) & curr
                        for mask, name in BUTTON_ITEMS:
                            if pressed & mask:
                                self._trigger_gesture(name)
                        last_buttons = curr
                    # 2. LT
                    lt_val = gp.bLeftTrigger
                    if lt_val > THRESHOLD_PRESS and not last_lt_state:
                        self._trigger_gesture("LT")
                        last_lt_state = True
                    elif lt_val < THRESHOLD_RELEASE:
                        last_lt_state = False
                    # 3. RT
                    rt_val = gp.bRightTrigger
                    if rt_val > THRESHOLD_PRESS and not last_rt_state:
                        self._trigger_gesture("RT")
                        last_rt_state = True
                    elif rt_val < THRESHOLD_RELEASE:
                        last_rt_state = False
                    time.sleep(0.01) # 100Hz
                else:
                    if self.hasGamepad:
                        self.hasGamepad = False
                        log.info("Gamepad disconnected")
                    # We did not find gamepad, have a good rest
                    time.sleep(5)
            except Exception:
                log.debugWarning("Gamepad poll cycle failed", exc_info=True)
                time.sleep(2)

    def _trigger_gesture(self, button_name):
        try:
            gesture = GamepadGesture(button_name)
            queueHandler.queueFunction(
                queueHandler.eventQueue, 
                inputCore.manager.executeGesture, 
                gesture
            )
        except Exception as e:
            log.error(f"Gamepad gesture execution failed: {e}")

    def terminate(self):
        self._terminate = True
        super().terminate()